from unittest import TestCase
from unittest.mock import call, MagicMock, Mock, patch

from intenthandlers.hue.lightsinroomonoffhandler import LightsInRoomOnOffHandler
from core.intent import Intent
from philipshue.huemanager import Group


class TestLightsInRoomOnOffHandler(TestCase):

    @patch("intenthandlers.hue.lightsinroomonoffhandler.HueManager")
    def test_get_intent_definitions(self, mocked_hue_manager):
        mocked_hue_manager.groups.return_value = [Group("Test", 1), Group("Test2", 2)]
        room_on_off_handler = LightsInRoomOnOffHandler()
        intent_definition = room_on_off_handler.intent_definitions[0]
        self.assertEqual("TurnLightsInRoomOnOff", intent_definition.name)
        self.assertEqual(1, len(intent_definition.sentences))
        self.assertEqual(3, len(intent_definition.sentences[0]))

    @patch('intenthandlers.hue.lightsinroomonoffhandler.HueManager')
    def test_handle_intent(self, hue_manager):
        hue_manager_instance = hue_manager.return_value
        intent = Intent("TurnLightsInRoomOnOff", "Turn the lights in the Living Room on",
                        parameters={"Room": "Living room", "OnOff": "On"})
        room_on_off_handler = LightsInRoomOnOffHandler()
        hue_manager_instance.get_group_by_name = Mock(return_value=Group("Living room", 13))
        hue_manager_instance.send_room_command_to_bridge = MagicMock()

        room_on_off_handler.handle_intent(intent)
        calls = [call("Living room", """{"on": true}""")]
        hue_manager_instance.send_room_command_to_bridge.assert_has_calls(calls)
