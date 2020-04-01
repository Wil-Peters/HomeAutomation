from unittest import TestCase
from unittest.mock import call, patch, Mock

from core.intenthandlermanager import IntentHandlerManager
from core.intentdefinition import IntentDefinition
from rhasspy.intentreceiver import RhasspyIntentReceiver


class TestIntentReceiverIntentHandlerManagerIntegration(TestCase):
    _intent_string = """{
                               "intent": {
                                   "name": "Test",
                                   "confidence": 1.0
                               },
                               "text": "test text",
                               "raw_text": "test text",
                               "recognize_seconds": 0.0031121610081754625,
                               "tokens": ["test", "text"],
                               "raw_tokens": ["test", "text"],
                               "speech_confidence": 1,
                               "wakeId": "",
                               "siteId": "default",
                               "time_sec": 0.012903928756713867
                           }
                       """

    def test_new_intent(self):
        mock_intent_handler = Mock()
        mock_intent_handler.intent_definitions = [IntentDefinition("Test", "Test text")]

        intent_handler_manager = IntentHandlerManager()
        intent_receiver = RhasspyIntentReceiver()

        intent_receiver.attach(intent_handler_manager)

        intent_handler_manager.subscribe_intent_handler(mock_intent_handler)

        response = intent_receiver.handle_new_intent(self._intent_string)
        expected_response = '{"intent": "Test", "time_sec": 0.0}'
        self.assertEqual(expected_response, response)
