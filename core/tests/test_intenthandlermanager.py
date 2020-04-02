from unittest import TestCase
from unittest.mock import MagicMock, Mock

from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intenthandlermanager import IntentHandlerManager


class TestIntentManager(TestCase):

    def test_dispatch_intent(self):
        mock_intent_handler = Mock()
        mock_intent_handler.intent_definitions = [IntentDefinition("test", "Test text")]
        mock_intent_handler.handle_intent = MagicMock()

        intent_manager = IntentHandlerManager()
        intent_manager.subscribe_intent_handler(mock_intent_handler)

        intent_manager.update(Intent('test', {}))

        mock_intent_handler.handle_intent.assert_called_once()

    def test_dispatch_unknown_intent(self):
        intent_manager = IntentHandlerManager()
        try:
            intent_manager.update(Intent("unknown", {}))
        except KeyError:
            self.fail("dispatch_intent raised KeyError unexpectedly")

    def test_get_all_intent_definitions(self):
        mock_intent_handler_1 = Mock()
        mock_intent_handler_1.intent_definitions = [IntentDefinition("test1", "Test text")]
        mock_intent_handler_2 = Mock()
        mock_intent_handler_2.intent_definitions = [IntentDefinition("test2", "Test text")]

        intent_manager = IntentHandlerManager()

        intent_manager.subscribe_intent_handler(mock_intent_handler_1)
        intent_manager.subscribe_intent_handler(mock_intent_handler_2)

        self.assertEqual(2, len(intent_manager.get_intent_definitions()))

    def test_handle_exception_in_intent_handler(self):
        mock_intent_handler = Mock()
        mock_intent_handler.intent_definitions = [IntentDefinition("test", "Test text")]
        mock_intent_handler.handle_intent = Mock(side_effect=KeyError("Shit happened"))

        intent_manager = IntentHandlerManager()

        intent_manager.subscribe_intent_handler(mock_intent_handler)

        try:
            intent_manager.update(Intent("test", {}))
        except KeyError:
            self.fail("IntentHandlerManager.update() unexpectedly raised a KeyError")

    def test_speaker_is_called_when_present(self):
        mock_intent_handler = Mock()
        mock_intent_handler.intent_definitions = [IntentDefinition("test", "Test text")]
        mock_intent_handler.handle_intent = Mock(return_value="Speak this text")

        speaker = Mock()

        intent_manager = IntentHandlerManager(speaker)
        intent_manager.subscribe_intent_handler(mock_intent_handler)

        intent_manager.update(Intent("test", {}))
        speaker.speak_text.assert_called_once()

