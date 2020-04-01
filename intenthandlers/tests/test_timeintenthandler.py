import time

from unittest import TestCase

from core.intent import Intent
from core.intenthandlermanager import IntentHandlerManager
from intenthandlers.timeintenthandler import TimeIntentHandler


class TestTimeIntentHandler(TestCase):

    def test_get_intent_definitions(self):
        time_intent_handler = TimeIntentHandler()
        intent_definitions = time_intent_handler.intent_definitions

        self.assertEqual(1, len(intent_definitions))

        sentences = intent_definitions[0].sentences
        self.assertEqual(1, len(sentences))
        self.assertEqual(1, len(sentences[0]))
        self.assertEqual("What time is it", sentences[0][0])

    def test_handle_intent(self):
        localtime = time.localtime()
        time_string = time.strftime("%H:%M", localtime)
        expected_response = "It is currently {} o'clock".format(time_string)

        intent = Intent("GetTime", {})
        intent_manager = IntentHandlerManager()

        time_intent_handler = TimeIntentHandler()
        intent_manager.subscribe_intent_handler(time_intent_handler)

        response = time_intent_handler.handle_intent(intent)
        self.assertEqual(expected_response, response)
