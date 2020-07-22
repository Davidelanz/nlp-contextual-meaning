<p align="center"> 
   <img width="200" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/logo.png?raw=true">
</p>

___

Website: [davidelanz.github.io/nlp-contextual-meaning](https://davidelanz.github.io/nlp-contextual-meaning/)

**Documentation**: [nlp-contextual-meaning.readthedocs.io](https://nlp-contextual-meaning.readthedocs.io/)

___

## Getting started

### Setting up DialogFlow

Follow the guide at
[https://cloud.google.com/dialogflow/docs/quick/setup](https://cloud.google.com/dialogflow/docs/quick/setup)
in order to set up the connection between the Python client and DialogFlow.
Briefly:

1. Start creating a new DialogFlow agent and the related Google project:

<img width="500" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/create_agent.png?raw=true">

Now, you should have an empty agent with the only `Default` intent:

<img width="500" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/empty_agent.png?raw=true">

2. Go to tour [Google Cloud Platform](https://console.cloud.google.com/)
   console. You should find the related project:

<img width="700" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/googlecloud_project.png?raw=true">

3. Following the instructions in
   [https://cloud.google.com/dialogflow/docs/quick/setup](https://cloud.google.com/dialogflow/docs/quick/setup),
   create a Service Account fitting the Dialogflow Agent and
   download the JSON key.

   > **IMPORTANT:** the Service Account has to be a **"DialogFlow API Admin"**
   > one, not a "DialogFlow API Client" or others. Admin rights are
   > needed for [Botium validation](#use-botium-for-identification-accuracy)

4. The JSON key shoud be saved in the root folder of this project
   (the same as this README and the `client.py` file) and
   called `google_key.json`. It shoud present the following fields:

```json
{
  "type": "service_account",
  "project_id": ,
  "private_key_id": ,
  "private_key": ,
  "client_email": ,
  "client_id": ,
  "auth_uri": ,
  "token_uri": ,
  "auth_provider_x509_cert_url": ,
  "client_x509_cert_url":
}
```

5. Install and configure then your Google Cloud SDK
   (see [https://cloud.google.com/sdk/docs](https://cloud.google.com/sdk/docs)).

### The `settings.json` file

The `settings.json` file containts information about the CSVdataset file name,
the folder in which export the intents in JSON format (from the CSV dataset)
and the language code of the agent (e.g. `"it"`,`"en-US"` etc...).
For the use case already available in this repository, we have:

```json
{
  "dataset-file": "situations_it",
  "intents-folder": "dataset_json",
  "language": "it"
}
```

### Prepare the dataset

A dataset of Italian sentences linked to 21 situations (85 sentences for
each situations) is available at `situations_dataset_.csv`. In
order to train the DialogFlow agent, you have to:

1. Convert the CSV data into JSON data by running:

```
python dataset/csv_to_json.py
```

2. Upload the 21 `.json` files created to DialogFlow:

<img width="600" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/upload_intents.png?raw=true">

3. At the end, you should have a situation like the one here in the picture:

<img width="500" src="https://github.com/Davidelanz/nlp-contextual-meaning/blob/master/images/intents_uploaded.png?raw=true">

### Run a demo

To simply test the agent you can run the `agent.py` file as follows:

```
python agent.py -s "Ho davvero caldo"
```

The result would be something like
`"Ho davvero caldo" -> Intent: avere-caldo (score: 0.8965118527412415)`.
This means the DialogFlow agent identified the intent `avere-caldo`
from the sentence "Ho davvero caldo" with a confidence of almost 90%.

## Client

To run and test the client:

```
python client.py
```

Some interaction examples (log are available in the client-generated
`logs` folder after running the client):

```
-----------------------------------------------
\INPUT > ho caldo
Robot: Vuoi che apra la finestra? (Y/N) y
Robot: apro la finestra
-----------------------------------------------
\INPUT > ho caldo
Robot: Vuoi che apra la finestra? (Y/N) n
Robot: porto una bottiglia d'acqua
-----------------------------------------------
\INPUT > mi sto annoiando a morte
Robot: accendo la televisione
-----------------------------------------------
```

## Change the language

Recall that the language of the dataset and hence the context table
generated are in **Italian**, but the system can be easily adapted
to other languages given a dataset as follows:


<!--table-->
| INTENT NAME             | PARENT'S INTENT | IS PARENT |            | [LANGUAGE]            |
| ----------------------- | --------------- | --------- | ---------- | --------------------- |
| Default Fallback Intent |                 |           | answer     | [DEFAULT_ANSWER]      |
| &#160;                  |                 |           |            |                       |
| [INTENT_1]              |                 |           | user-input | [TRAINING_SENTENCE_1] |
| [INTENT_1]              |                 |           | user-input | [TRAINING_SENTENCE_2] |
| ...                     |                 |           | ...        | ...                   |
| [INTENT_1]              |                 |           | user-input | [TRAINING_SENTENCE_N] |
| &#160;                  |                 |           |            |                       |
| [INTENT_2]              |                 |           | user-input | [TRAINING_SENTENCE_1] |
| ...                     |                 |           | ...        | ...                   |
<!--endtable-->


The dataset has to be stored in `.csv` format with `;` separator. For example:

```
INTENT NAME;PARENT'S INTENT;IS PARENT?;;en-US
Default Fallback Intent;;answer;I haven't understood.
;;;;
overheat;;;user-input;so hot!
overheat;;;user-input;I'm dying of heat.
overheat;;;user-input;it's so hot!
overheat;;;user-input;it's too hot in this room.
overheat;;;user-input;How hot
;;;;
bug-in-room;;;user-input;Ew, a bug!
bug-in-room;;;user-input;Oh, God, there's a bug.
bug-in-room;;;user-input;Oh, my God, there's a bug!
bug-in-room;;;user-input;Dad, there's a huge bug in the room.
bug-in-room;;;user-input;How disgusting, a winged beast.
;;;;
boredom;;;user-input;Aren't you bored?
boredom;;;user-input;Bollocks, I'm bored.
boredom;;;user-input;This is so boring!
boredom;;;user-input;I'm so bored.
boredom;;;user-input;Let's do something, I'm dying of boredom.
;;;;
```

Then, the `context_table.json` file has to be changed as well. For example,
if we keep the same reactions as the one provided here, for the
example dataset we just saw we could have:

```json
{
  "reactions": [
    "I'll open the window",
    "I'll bring you a bottle of water",
    "I'll turn on the TV"
  ],
  "queries": [
    "Should I open the window?",
    "Should I bring you a bottle of water?",
    "Should I turn on the TV?"
  ],
  "default": ["I am sorry, I can't do a lot for you."],
  "r1": {
    "overheat": 0.1,
    "bug-in-room": 0.07,
    "boredom": 0
  },
  "r2": {
    "overheat": 0.02,
    "bug-in-room": 0.02,
    "boredom": 0
  },
  "r3": {
    "overheat": 0,
    "bug-in-room": 0,
    "boredom": 0.07
  }
}
```

## Use [Botium](https://github.com/codeforequity-at/botium-connector-dialogflow) for identification accuracy

### Setting up Botium

Requirements:

- Node.js (`sudo apt-get install nodejs`)
- NPM (`sudo apt-get install npm`)

We will need Botium CLI:

```
npm install -g botium-cli
npm install -g botium-connector-dialogflow
botium-cli init
```

Then, create a file `botium.json` in the working directory and add the
Google credentials for accessing your Dialogflow agent.
This [article](https://chatbotsmagazine.com/3-steps-setup-automated-testing-for-google-assistant-and-dialogflow-de42937e57c6)
shows how to retrieve all those settings
(you can find them in the `google_key.json` file as well).

```json
{
  "botium": {
    "Capabilities": {
      "PROJECTNAME": "<whatever>",
      "CONTAINERMODE": "dialogflow",
      "DIALOGFLOW_PROJECT_ID": "<google project id>",
      "DIALOGFLOW_CLIENT_EMAIL": "<service credentials email>",
      "DIALOGFLOW_PRIVATE_KEY": "<service credentials private key>"
    }
  }
}
```

To check the configuration, run the emulator (Botium CLI required)
to bring up a chat interface in your terminal window:

```
botium-cli emulator
```

Now that botium setup is ready, it’s time to run the benchmark. The
`botium-cli nlpanalytics` command runs NLP analytics with
on of these two algorithms:

- `validate` - run one-shot training and testing of NLP engine
- `k-fold` - run k-fold training and testing of NLP engine

See this
[article](https://chatbotslife.com/tutorial-benchmark-your-chatbot-on-watson-dialogflow-wit-ai-and-more-92885b4fbd48)
for further information.

### Prepare the data

We can extract the data - intents and utterances (user examples) -
from our already-trained DialogFlow automatically:

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google_key.json"
botium-cli nlpextract --config botium.json --convos dataset_botium --verbose
```

This command will write several text files to the `dataset_botium` directory
with filename pattern `intentname.utterances.txt`
(see [Botium Wiki](https://botium.atlassian.net/wiki/spaces/BOTIUM/pages/48922633/Composing+in+Text+files)).
First line of the file contains the intent name, following lines are the
utterances (user examples). For example:

```
temperature
Is it me or it is hot here?
What's the current temperature?
What’s the current temperature?
```

### Validate data

To validate the dataset with wich we trained our DialogFlow agent, we
run the stratified k-fold cross-validation for the data against
the DialogFlow agent (with k=5, meaning one fifth is used for testing,
four fifth are used for training):

```
botium-cli nlpanalytics k-fold -k 5 --config botium.json
```

Botium will create a separate DialogFlow agent workspace for all test runs
and clean it up afterwards. The original workspace - if existing - won’t
be affected.

The benchmark takes some time, and the results are printed out when ready -
for each of the 5 rounds and the total average over all rounds:

```
############# Summary #############
K-Fold Round 1:
```

> Note that Botium supports
> [other platforms](https://botium.atlassian.net/wiki/spaces/BOTIUM/pages/360553/Botium+Connectors).
> It is possible then to compare
> the accuracies of these platform given a certain dataset.

## References

- Lanza, Menicatti, Sgorbissa.
  "Abductive Recognition of Context-dependent
  Utterances in Human-robot Interaction,'' in _2020 IEEE/RSJ International_
  _Conference on Intelligent Robots and Systems (IROS)_, Las Vegas, USA.

- Lanza.
  "Context-dependent meanings recognition in human-robot interaction'',
  _Bachelor's Thesis_, University of Genoa, 2018
  (**in italian**)
  [[pdf](https://github.com/Davidelanz/nlp-contextual-meaning/references/Lanza2018_BachelorThesis_IT.pdf)]
