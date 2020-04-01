"""This module contains the Intent class, which is a representation of an intent from the user
towards their voice assistant"""
from typing import Dict


class Intent:
    """Represents an Intent as spoken by the user towards their voice assistant."""
    def __init__(self, name: str, full_intent_string: str, parameters: Dict[str, str] = {}):
        self._name = name
        self._parameters = parameters
        self._full_intent_string = full_intent_string

    @property
    def name(self) -> str:
        """Name of the intent"""
        return self._name

    @property
    def parameters(self) -> Dict[str, str]:
        """Dictionary containing the parameters associated with an Intent.
        The dictionary typically contains a set of keywords and their responsive values,
        as they were given in the voice command by the user.

        Example:
            {
            "Room": "living room",
            "State": "on"
            }
        """
        return self._parameters

    @property
    def full_intent_string(self) -> str:
        """Contains the full sentence, as spoken by the user in their voice command.
        Example: "turn the lights in the living room on"
        """
        return self._full_intent_string
