"""This module contains the IntentHandler abstract base class, which can be used to define an
IntentHandler."""
from abc import ABC
from typing import List

from core.intent import Intent
from core.intentdefinition import IntentDefinition, Sentence


class IntentHandler(ABC):
    """
    The IntentHandler base class is meant to provide a common interface for all classes that
    handle Intents.

    It defines 1 method and 1 property:
    - handle_intent
    - intent_definitions

    NOTE: Currently all IntentHandlers have to be subscribed to the IntentHandlerManager.
    This is done in the IntentHandlerManagerFactory class in factories.intenthandlermanagerfactory.
    """
    _intent_definitions: List[IntentDefinition] = []

    def __init__(self):
        pass

    @property
    def intent_definitions(self) -> List[IntentDefinition]:
        """Returns a List of IntentDefinitions. An IntentDefinition defines which Intents an
        IntentHandler can handle. For more information see the
        core.intentdefinition.IntentDefinition class"""
        return self._intent_definitions

    def handle_intent(self, intent: Intent) -> str:
        """Is called by the IntentHandlerManager when it receives an Intent, of which the
        IntentHandler published an IntentDefinition"""
        pass

    @staticmethod
    def _create_one_string_sentence_intent_definition(intent_name: str, sentence_string: str) -> \
            IntentDefinition:
        """Creates the most basic of IntentDefinitions, those consisting of only one single
        string"""
        intent_definition = IntentDefinition(intent_name)
        sentence = Sentence()
        sentence.add_string(sentence_string)
        intent_definition.add_sentence(sentence)
        return intent_definition
