import logging
from typing import Dict, List

from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intentdefinitionsource import IntentDefinitionSource
from core.intenthandler import IntentHandler
from core.newintentobserver import NewIntentObserver
from core.speaker import Speaker
from core.utils.classname import fullname


class IntentHandlerManager(IntentDefinitionSource, NewIntentObserver):
    """The IntentHandlerManager is the central hub of the program. It receives new Intents from a
    NewIntentSubject and passes the Intent to the appropriate IntentHandler.

    The IntentHandlerManager also directs responses from the IntentHandlers to the Speaker."""

    def __init__(self, speaker: Speaker = None):
        self._logger = logging.getLogger(fullname(self))
        self._intent_handlers: Dict[str, IntentHandler] = {}
        self._speaker = speaker

    def update(self, intent: Intent) -> None:
        """Implements NewIntentObserver.update. Gets called when the NewIntentSubject has a new
        Intent for its observers."""
        if intent.name in self._intent_handlers.keys():
            text_to_speak = self._handle_intent(intent)
        else:
            self._logger.info("Intent Manager: no intenthandler registered for: %s", intent.name)
            text_to_speak = "I do no know how to %s" % intent.full_intent_string
        if self._speaker:
            self._speaker.speak_text(text_to_speak)

    def _handle_intent(self, intent) -> str:
        result = ""
        self._logger.info("Intent Manager: dispatching intenthandlers '%s'", intent.name)
        try:
            response = self._intent_handlers[intent.name].handle_intent(intent)
            if response:
                result = response
        except Exception as exception:
            self._logger.info("Exception occurred in intenthandlers handler [%s]: %s",
                              fullname(self._intent_handlers[intent.name]), exception)
            result = "Something went wrong while handling your request: %s" % \
                     intent.full_intent_string
        return result

    def subscribe_intent_handler(self, intent_handler: IntentHandler):
        """Subscribe a new IntentHandler that can handle Intents. Stores the IntentDefinitions
        exposed by the IntentHandler, so they can be used later on when a new Intent comes in.
        Only the IntentHandler which exposes a certain IntentDefinition will be called when
        update() is called with that Intent"""
        for intent_definition in intent_handler.intent_definitions:
            self._logger.info("Added subscription on intenthandlers [%s] for %s",
                              intent_definition.name, intent_handler)
            self._intent_handlers[intent_definition.name] = intent_handler

    def get_intent_definitions(self) -> List[IntentDefinition]:
        """Returns all IntentDefinition of all IntentHandlers which are subscribed to the
        IntentHandlerManager"""
        all_intent_definitions = []
        for intent_handler in self._intent_handlers.values():
            intent_definitions = intent_handler.intent_definitions
            all_intent_definitions.extend(intent_definitions)
        return all_intent_definitions
