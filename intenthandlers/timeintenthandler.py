import time
from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intenthandler import IntentHandler


class TimeIntentHandler(IntentHandler):

    def __init__(self):
        super().__init__()
        get_time_intent_definition = self.create_get_time_intent_definition()
        self._intent_definitions = [get_time_intent_definition]

    def create_get_time_intent_definition(self) -> IntentDefinition:
        return self._create_one_string_sentence_intent_definition("GetTime", "What time is it")

    @staticmethod
    def handle_intent(intent: Intent) -> str:
        localtime = time.localtime()
        time_string = time.strftime("%H:%M", localtime)
        return "It is currently {} o'clock".format(time_string)
