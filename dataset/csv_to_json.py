import json
import os

# Load settings json file
with open("settings.json", encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

DATASET_FILE = settings["dataset-file"]
INTENTS_FOLDER = settings["intents-folder"]
DEFAULT_LANGUAGE = settings["language"]
DELIMITER = ";"


def getFollowups(language, followup):
    followups = []

    for sentence in settings["dialogflow"]["followups"][language][followup]:
        followups.append(
            {
                "data": [
                    {
                        "text": sentence
                    }
                ]
            }
        )
    return followups


def getDataType(par_name, parameters):
    for parameter in parameters:
        if parameter["name"] == par_name:
            return parameter["dataType"]
    return None


def retrieveData():
    intent_dict = {}

    # Read the source .csv file
    current_dir = os.path.dirname(__file__)
    intents_path = os.path.join(current_dir, DATASET_FILE + ".csv")
    with open(intents_path, encoding='utf-8') as intent_file:
        content = intent_file.readlines()

    # Store data in a dictionary
    first_row = content[0][:-1].split(DELIMITER)
    languages = first_row[4:]
    intent_list = {}

    # Loop through columns (languages)
    for index, language in enumerate(languages):
        col = index + 4
        intent_dict[language] = {}
        intent_list[language] = []

        # Loop through rows (intents)
        for line in content[1:]:
            row = line[:-1].split(DELIMITER)
            intent = row[0]
            parent = row[1]
            is_parent = True if row[2] == "x" else False
            type = row[3]
            text = row[col]

            if intent != "":
                if intent not in intent_list[language]:
                    intent_list[language].append(intent)
                    intent_dict[language][intent] = {"parent": parent,
                                                     "isParent": is_parent,
                                                     "user-input": [],
                                                     "myPersonalId": [],
                                                     "answer": [],
                                                     "variable": []}
                if row[col] != "":
                    intent_dict[language][intent][type].append(text)
                    # : add user-inputs and answers
                    if type == "user-input":
                        intent_ID = intent
                        uinput_ID = str(len(
                            intent_dict[language][intent][type])-1).zfill(3)
                        ID = "%s-%s-%s" % (intent_ID, uinput_ID, language)
                        intent_dict[language][intent]["myPersonalId"].append(
                            ID)

    print(json.dumps(intent_dict, sort_keys=True,
                     indent=4, separators=(',', ': ')))
    return intent_dict
# ------------------------------------------------------


def createJson(intent_dict):
    # Loop through languages
    for language in intent_dict.keys():

        # Loop through intents
        for intent in intent_dict[language].keys():
            userSays = []
            # uploaded = []

            # If the json file of the intent already exists, retrieve the
            #  user inputs first
            intent_json = os.path.join(
                INTENTS_FOLDER, language, intent + "_" + language + ".json")
            # if os.path.isfile(intent_json):
            #   with open(intent_json, encoding='utf-8') as json_file:
            #     loaded_intent = json.load(json_file)
            #
            #   userSays = loaded_intent["userSays"]
            #   for sentence in userSays:
            #     if sentence["alreadyUploaded"] == True:
            #       uploaded.append(sentence["myPersonalId"])
            speech = intent_dict[language][intent]["answer"]
            inputs = intent_dict[language][intent]["user-input"]
            parent = intent_dict[language][intent]["parent"]
            is_parent = intent_dict[language][intent]["isParent"]
            IDs = intent_dict[language][intent]["myPersonalId"]
            variables = intent_dict[language][intent]["variable"]
            # param_list = []
            parameters = []

            for variable in variables:
                var_name = variable.split('*')[0]
                var_type = variable.split('*')[1]
                var_value = "$" + var_name
                var_required = False
                var_prompts = []

                if len(variable.split('*')) == 3:
                    var_required = True
                    prompts = variable.split('*')[2]
                    for prompt in prompts.split('+'):
                        var_prompts.append(prompt)
                parameters.append({
                    "required": var_required,
                    "dataType": var_type,
                    "name": var_name,
                    "value": var_value,
                    "prompts": var_prompts,
                    "isList": False
                })

            for index, input in enumerate(inputs):
                # if not IDs[index] in uploaded:
                input_parts = input.split('#')
                data = []
                for part in input_parts:
                    if "*" in part:
                        part = part.split('*')
                        text = part[0]
                        name = part[1]
                        # datatype = part[2]
                        #
                        # if not part[1] in param_list:
                        #
                        #   if len(part) == 4:
                        #     required = True
                        #     prompts = part[3].split('+')
                        #   else:
                        #     required = False
                        #     prompts = []
                        #
                        #   param_list.append(name)
                        #   parameters.append({
                        #     "required": required,
                        #     "dataType": datatype,
                        #     "name": name,
                        #     "value": "$%s" % name,
                        #     "prompts": prompts,
                        #     "isList": False
                        #   })
                        data.append({
                            "text":  text,
                            "alias": name,
                            "meta":  getDataType(name, parameters),
                            "userDefined": True})
                    else:
                        data.append({"text": part})
                new_input = {
                    "myPersonalId": IDs[index],
                    # "alreadyUploaded": False,
                    "data": data,
                    "isTemplate": False,
                    "count": 0
                }
                userSays.insert(0, new_input)

            template = {
                "name": intent,
                "auto": True,
                "contexts": [],
                "templates": [],
                "responses": [
                    {
                        "parameters": parameters,
                        "messages": [
                            {
                                "type": 0,
                                "speech": speech
                            }
                        ],
                        "defaultResponsePlatforms": {},
                        "speech": []
                    }
                ],
                "userSays": userSays
            }
            if not parent == "":
                template["contexts"] = [parent + "-followup"]
                template["responses"][0]["action"] = (
                    parent + "." + intent).replace(" ", "")
                if intent.split(" - ")[1] == "yes":
                    template["userSays"] = getFollowups(
                        DEFAULT_LANGUAGE, "yes")
                elif intent.split(" - ")[1] == "no":
                    template["userSays"] = getFollowups(DEFAULT_LANGUAGE, "no")
            if is_parent:
                template["responses"][0]["resetContexts"] = False
                template["responses"][0]["affectedContexts"] = [
                    {
                        "name": intent + "-followup",
                        "parameters": {},
                        "lifespan": 2
                    }
                ]
            if intent == "Default Fallback Intent":
                template["responses"][0]["action"] = "input.unknown"
                template["fallbackIntent"] = True
            dest_folder = os.path.join(INTENTS_FOLDER, language)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            with open(intent_json, 'w', encoding='utf-8') as myfile:
                json.dump(template, myfile)


if __name__ == '__main__':
    intent_dictionary = retrieveData()
    createJson(intent_dictionary)
    print("Intents converted to JSON")
