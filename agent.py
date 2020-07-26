import logging
import json
import argparse
import time
import os
import dialogflow_v2 as dialogflow


class Agent():
    """The ``Agent`` class provides the methods to connect to
    DialogFlow APIs and perform basic intent queries.

    Attributes
    ----------
    language : string
        Agent's language code (e.g. ``"en-US"``).
    project_id : string
        DialogFlow's API project ID.
    session_client : dialogflow.SessionsClient
        SessionsClient class to manage API sessions.
    """

    def __init__(self):
        self.language = "it"
        logging.debug(f"agent language: {self.language}")

        # Set environment variable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
            os.getcwd() + "/client_key.json"
        logging.debug("env variable GOOGLE_APPLICATION_CREDENTIALS={}".format(
            os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        ))

        # Load project_id from authorization key
        key_file = "client_key.json"
        logging.debug(f"loading project_id from {key_file}")
        with open(key_file) as f:
            key = json.load(f)

        # Start a session
        self.project_id = key["project_id"]
        self.session_client = dialogflow.SessionsClient()
        logging.debug('session client created')

    def get_intent_score(self, sentence):
        """Given a sentence, detects a related intent with a certain
        confidence score.

        Parameters
        ----------
        sentence : string
            Input sentence to be processed

        Returns
        ----------
        string, float
            A string containing the detected intent and the correspondent
            confidence score.

        Examples
        --------
        >>> agent = Agent()
        >>> agent.get_intent_score("It's hot")
        ("overheat", 0.8965118527412415)
        """
        # Create Text and Query Input objects
        text_input = dialogflow.types.TextInput(
            text=sentence, language_code=self.language)
        query_input = dialogflow.types.QueryInput(text=text_input)

        # Open a session.
        # Using the same `session_id` between requests allows
        #   continuation of the conversation.
        session_id = time.strftime("%Y%m%d%H%M%S")
        session = self.session_client.session_path(self.project_id, session_id)
        logging.debug(f'session path={session}')

        # Obtain the response and extract intent and confidence score
        response = self.session_client.detect_intent(session, query_input)
        intent = response.query_result.intent.display_name
        score = response.query_result.intent_detection_confidence
        # response.query_result.fulfillment_text

        logging.debug(f"Query text: {response.query_result.query_text}")
        logging.debug(f"Detected intent: {intent} (score: {score})")

        return intent, score


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--sentence",
                        type=str,
                        required=True,
                        help="The sentence you want to submit to the agent")
    args = parser.parse_args()

    test_sentence = args.sentence

    agent = Agent()

    intent, score = agent.get_intent_score(test_sentence)
    print(f"\"{test_sentence}\" -> Intent: {intent} (score: {score})")
