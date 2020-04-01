from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intenthandler import IntentHandler


class UnknownIntentHandler(IntentHandler):

    def __init__(self):
        super().__init__()
        self._intent_definitions = [IntentDefinition("")]

    def handle_intent(self, intent: Intent) -> str:
        return "I'm sorry, but I could not understand what you asked."
