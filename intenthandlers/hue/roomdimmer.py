import json

from core.intent import Intent
from core.intentdefinition import IntentDefinition, Sentence, SentenceParameter
from core.intenthandler import IntentHandler
from philipshue.huemanager import HueManager


class RoomDimmer(IntentHandler):

    UP_DOWN = "UpDown"
    UP = "Up"
    DOWN = "Down"
    IN_DECREASE = "InDecrease"
    INCREASE = "Increase"
    DECREASE = "Decrease"
    ROOM = "Room"

    def __init__(self):
        super().__init__()
        self._hue_manager = HueManager()
        dim_room_intent_definition = self.get_dim_room_intent_definition()
        self._intent_definitions = [dim_room_intent_definition]

    def get_dim_room_intent_definition(self):
        dim_room = IntentDefinition("DimRoom")

        sentence = Sentence()
        sentence.add_string("Dim the lights in the")

        room_names = [room.name for room in self._hue_manager.groups]
        room_parameter = SentenceParameter(self.ROOM, True, possible_values=room_names)
        sentence.add_parameter(room_parameter)
        parameter2 = SentenceParameter(self.UP_DOWN, True, possible_values=[self.UP, self.DOWN])
        sentence.add_parameter(parameter2)

        dim_room.add_sentence(sentence)

        sentence2 = Sentence()
        indecrease_parameter = SentenceParameter(self.IN_DECREASE, True, possible_values=[
            self.INCREASE, self.DECREASE])
        sentence2.add_parameter(indecrease_parameter)
        sentence2.add_string("the brightness in the")
        sentence2.add_parameter(room_parameter)
        dim_room.add_sentence(sentence2)

        return dim_room

    def handle_intent(self, intent: Intent) -> str:
        bri_inc = 20
        room = intent.parameters[self.ROOM]
        response = ""
        if self.UP_DOWN in intent.parameters:
            direction = intent.parameters[self.UP_DOWN]
            if intent.parameters[self.UP_DOWN] == self.DECREASE:
                bri_inc = -20
            response = "Dimming the lights in the {} {}".format(room, direction)

        elif self.IN_DECREASE in intent.parameters:
            action = "Increasing"
            if intent.parameters[self.IN_DECREASE] == self.DECREASE:
                bri_inc = -20
                action = "Decreasing"
            response = "{} the brightness of the lights in the {}".format(action, room)
        payload = {"bri_inc": bri_inc}
        self._hue_manager.send_room_command_to_bridge(intent.parameters[self.ROOM], json.dumps(
            payload))
        return response
