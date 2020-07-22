import operator
import logging
import nltk.corpus
import json
import time
import os
from agent import Agent


class Client:
    """The ``Client`` class is the backends which receives the User
    input and performs situation identification and reaction selection 
    through an abductive inference process (given contextual data).

    To start interacting with the client, run the following command:

    .. code-block:: 

        python client.py

    An example interaction is:

    .. code-block::

        \INPUT > It's hot here
        Robot: Should I open the window? (Y/N) n
        Robot: I'll bring you a bottle of water.


    Attributes
    ----------
    agent : Agent
        DialogFlow agent.
    context : dict
        Dictionary containing context table and reactions information.
        For example:

        .. code-block:: json

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


    """

    def __init__(self):
        # Set logging file
        try:
            os.makedirs("logs")
        except FileExistsError:
            pass
        now = time.strftime("%Y%m%d-%H%M%S")
        logging.basicConfig(filename=f'logs/{now}.log', level=logging.DEBUG)

        # DialogFlow agent
        self.agent = Agent()

        # Contextual table
        with open("context_table.json") as f:
            self.context = json.load(f)

    def std_situation_analysis(self, sentence):
        """Given a sentence, simply returns DialogFlow identified intent

        Parameters
        ----------
        sentence : string
            Input sentence to be processed

        Returns
        ----------
        string
            A string containing the detected situation.

        Examples
        --------
        >>> client = Client()
        >>> client.std_situation_analysis("It's hot")
        "overheat"

        """
        intent, score = self.agent.get_intent_score(sentence)
        logging.debug(
            f"standard analysis result: situation={intent} (score={score})")
        return intent

    def deep_situation_analysis(self, sentence):
        """Given a sentence, breaks it and send the single words to DialogFlow.
        Then, it returns the intent of the word with the maximum score.
        
        Parameters
        ----------
        sentence : string
            Input sentence to be processed

        Returns
        ----------
        string
            A string containing the detected situation.
        
        """
        # Breaks the sentence into single words
        sentence = sentence.lower()
        sentence = sentence.split()

        # Preparing output
        out_intent = []
        out_score = []
        out_word = []  # The word which contributed to the intent detection

        # Preparing stopwords
        stoplist = nltk.corpus.stopwords.words('italian')
        # and clean sentence from stopwords
        sentence = [word for word in sentence if word not in stoplist]

        # Get Dialogflow response and extract relevant information
        for word in sentence:
            intent, score = self.agent.get_intent_score(word)
            # If an intent was detected, extract necessary data
            if intent != 'Default Fallback Intent':
                out_intent.append(intent)
                out_score.append(score)
                out_word.append(word)
                logging.debug(f"deep analysis: word={word}, \
situation={intent} (score={score})")

        # Return the intent of the work with the maximum score
        if (out_score == []):
            # If no intent was detected, return the Default one
            return "Default Fallback Intent"
        else:
            index, _ = max(enumerate(out_score), key=operator.itemgetter(1))
            logging.debug(f"deep analysis result: \
situation={out_intent[index]} (score={score})")
            return out_intent[index]

    def ask_question(self, question):
        """Poses a Y/N question to the user.

        Note
        ---------
        This function loops until the user does not give a Y/N answer.

        Parameters
        ----------
        question : string
            The question to be displayed.

        Returns
        ----------
        string
            Returns the answer as 'y' or 'n'.
        """
        while True:
            answer = input(question + " (Y/N) ")
            logging.debug(question + " (Y/N) ")
            if (answer == "Y" or answer == "y"):
                logging.debug('y')
                return 'y'
            elif (answer == "N" or answer == "n"):
                logging.debug('n')
                return 'n'
            else:
                print("  ***rispondere con Y o N***   ")
                logging.debug("  ***rispondere con Y o N***   ")

    def main(self):
        """Starts the client workflow."""
        now = time.strftime("%Y%m%d-%H%M%S")
        logging.debug(f"client activity started at {now}")

        print("""\n-----------------------------------------------""")
        user_input = input("\\INPUT > ")
        logging.debug(f"\\INPUT > {user_input}")

        logging.debug("identifying situation via standard analysis")
        situation = self.std_situation_analysis(user_input)

        if (situation == 'Default Fallback Intent'):
            logging.debug("situation not identified, deepAnalysis started")
            situation = self.deep_situation_analysis(user_input)

        logging.debug(f"situation identified: {situation}")

        if (situation == 'Default Fallback Intent'):
            default = self.context["default"]
            print(f"Robot: {default}")
            logging.debug(f"Robot: {default}")
            return

        # get the contextual probabilities for detected intent
        pr1 = self.context["r1"][situation]
        pr2 = self.context["r2"][situation]
        pr3 = self.context["r3"][situation]
        probs = [pr1, pr2, pr3]

        while True:

            # Get the max probability index
            max_idx = [idx for idx, p in enumerate(
                probs) if p == max(probs)]

            logging.debug(f"Probabilities: {probs}")

            # If there is only one possible reaction
            if len([p for p in probs if p != 0]) == 1:
                logging.debug("only one possible reaction")
                reaction = self.context["reactions"][max_idx[0]]
                print(f"Robot: {reaction}")
                logging.debug(f"Robot: {reaction}")
                break  # Exit the loop when reacting

            # If we have to disambiguate between multiple probabilities
            else:
                logging.debug("start disambiguating")
                query = self.context["queries"][max_idx[0]]
                if self.ask_question(f"Robot: {query}") == 'y':
                    reaction = self.context["reactions"][max_idx[0]]
                    print(f"Robot: {reaction}")
                    logging.debug(f"Robot: {reaction}")
                    break  # Exit the loop when reacting
                else:
                    probs[max_idx[0]] = 0

        print("""-----------------------------------------------\n""")


if __name__ == '__main__':
    # nltk.download('stopwords')

    client = Client()
    client.main()
