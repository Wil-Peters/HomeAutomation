from unittest import TestCase
from unittest.mock import MagicMock, Mock

from rhasspy.intentreceiver import RhasspyIntentReceiver


class TestRhasspyIntentReceiver(TestCase):
    intent_string = """{
                            "intent": {
                                "name": "TurnLightsInRoomOnOff",
                                "confidence": 1.0
                            },
                            "entities": [{
                                    "entity": "room",
                                    "value": "study",
                                    "raw_value": "study",
                                    "start": 23,
                                    "raw_start": 23,
                                    "end": 28,
                                    "raw_end": 28,
                                    "tokens": ["study"],
                                    "raw_tokens": ["study"]
                                }, {
                                    "entity": "state",
                                    "value": "on",
                                    "raw_value": "on",
                                    "start": 29,
                                    "raw_start": 29,
                                    "end": 31,
                                    "raw_end": 31,
                                    "tokens": ["on"],
                                    "raw_tokens": ["on"]
                                }
                            ],
                            "text": "turn the lights in the study on",
                            "raw_text": "turn the lights in the study on",
                            "recognize_seconds": 0.0031121610081754625,
                            "tokens": ["turn", "the", "lights", "in", "the", "study", "on"],
                            "raw_tokens": ["turn", "the", "lights", "in", "the", "study", "on"],
                            "speech_confidence": 1,
                            "slots": {
                                "room": "study",
                                "state": "on"
                            },
                            "wakeId": "",
                            "siteId": "default",
                            "time_sec": 0.012903928756713867
                        }
                    """

    def test_create_intent_object_and_dispatch_to_listeners(self):
        try:
            rhasspy_intent_receiver = RhasspyIntentReceiver()
            mock_new_intent_observer = Mock()
            mock_new_intent_observer.update = MagicMock(return_value=("Test response", False))

            rhasspy_intent_receiver.attach(mock_new_intent_observer)
            rhasspy_intent_receiver.handle_new_intent(self.intent_string)

            mock_new_intent_observer.update.assert_called_once()

            intent_in_mock_call = mock_new_intent_observer.update.call_args[0][0]
            self.assertEqual("TurnLightsInRoomOnOff", intent_in_mock_call.name)
            self.assertEqual({"room": "study", "state": "on"}, intent_in_mock_call.parameters)
        except KeyError:
            self.fail("create_intent_object raised an unexpected KeyError")
