<p align="center"> 
   <img width="200" src="images/logo.png">
</p>

## Contents

1. [Getting started](#getting-started)
   1. [Setting up DialogFlow](#setting-up-dialogflow)
   1. [The `settings.json` file](#the-settingsjson-file)
   1. [Prepare the dataset](#prepare-the-dataset)
   1. [Run a demo](#run-a-demo)
1. [Client](#client)
1. [Change the language](#change-the-language)
1. [References](#references)

## Getting started

### Setting up DialogFlow

Follow the guide at https://cloud.google.com/dialogflow/docs/quick/setup
(available also in the file [`dialogflow_quickstart.md`](dialogflow_quickstart.md)) in order to
set up the connection between the Python client and DialogFlow.
Briefly:

1. Start creating a new DialogFlow agent and the related Google project:

<img width="500" src="images/create_agent.png">

Now, you should have an empty agent with the only `Default` intent:

<img width="500" src="images/empty_agent.png">

2. Go to tour [Google Cloud Platform](https://console.cloud.google.com/)
   console. You should find the related project:

<img width="700" src="images/googlecloud_project.png">

3. Following the instructions in
   https://cloud.google.com/dialogflow/docs/quick/setup, create a Service
   Account fitting the Dialogflow Agent and download the JSON key.

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
   (see https://cloud.google.com/sdk/docs).

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

```linux
python dataset/csv_to_json.py
```

2. Upload the 21 `.json` files created to DialogFlow:

<img width="600" src="images/upload_intents.png">

3. At the end, you should have a situation like the one here in the picture:

<img width="500" src="images/intents_uploaded.png">

### Run a demo

To simply test the agent you can run the `agent.py` file as follows:

```linux
python agent.py -s "Ho davvero caldo"
```

The result would be something like
`"Ho davvero caldo" -> Intent: avere-caldo (score: 0.8965118527412415)`.
This means the DialogFlow agent identified the intent `avere-caldo`
from the sentence "Ho davvero caldo" with a confidence of almost 90%.

## Client

To run and test the client:

```linux
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

The dataset has to be stored in `.csv` format with `;` separator. For example:

```csv
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

## References

- Lanza, Menicatti, Sgorbissa. ``Abductive Recognition of Context-dependent
  Utterances in Human-robot Interaction,'' in _2020 IEEE/RSJ International_
  _Conference on Intelligent Robots and Systems (IROS)_, Las Vegas, USA.

- Lanza. 
  ``Context-dependent meanings recognition in human-robot interaction'',
  *Bachelor's Thesis*, University of Genoa, 2018
  (**in italian**)
  [[pdf](references/Lanza2018_BachelorThesis_IT.pdf)] 
