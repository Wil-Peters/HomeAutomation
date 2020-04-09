import json

from core.intent import Intent
from core.intentdefinition import IntentDefinition, SentenceBuilder, SetParameter
from core.intenthandler import IntentHandler
from philipshue.huemanager import HueManager


class LightsInRoomOnOffHandler(IntentHandler):

    ONOFF = "OnOff"
    ON = "On"
    OFF = "Off"
    ROOM = "Room"

    def __init__(self):
        IntentHandler.__init__(self)
        self._hue_manager = HueManager()
        room_on_off_intent_definition = self._get_room_on_off_intent_definition()
        self._intent_definitions = [room_on_off_intent_definition]

    def _get_room_on_off_intent_definition(self) -> IntentDefinition:
        room_on_off = IntentDefinition("TurnLightsInRoomOnOff")

        room_names = [room.name for room in self._hue_manager.groups]
        room_parameter = SetParameter(self.ROOM, True, possible_values=room_names)

        on_off_parameter = SetParameter(self.ONOFF, True, possible_values=[self.ON, self.OFF])

        sentence_builder = SentenceBuilder()
        sentence_builder.add_string("Turn the lights in the")\
            .add_parameter(room_parameter)\
            .add_parameter(on_off_parameter)

        sentence = sentence_builder.build()
        room_on_off.add_sentence(sentence)
        return room_on_off

    def handle_intent(self, intent: Intent) -> str:
        payload = {"on": intent.parameters[self.ONOFF].lower() == "on"}
        self._hue_manager.send_room_command_to_bridge(intent.parameters[self.ROOM], json.dumps(payload))
        room = intent.parameters[self.ROOM]
        on_off = intent.parameters[self.ONOFF].lower()
        return "Turning the lights in the {} {}".format(room, on_off)
