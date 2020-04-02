"""This module contains classes that can be used to construct an IntentDefinition, a kind of
blueprint for the Intent an IntentHandler can handle."""
from __future__ import annotations
from typing import List


class SentenceParameter(object):
    """Represents a part of the Sentence where the user can give a certain "input"."""
    def __init__(self, name: str, return_value=False, possible_values: List[str] = []):
        self._name = name
        self._return_value = return_value
        self._possible_values = possible_values

    @property
    def name(self) -> str:
        """Name of the parameter. Can be used in the Intent to identify which parameter
        gets which value, based on the users input."""
        return self._name

    @property
    def return_value(self) -> bool:
        """Add the value of this parameter in the Intent?
        """
        return self._return_value

    @property
    def possible_values(self) -> List[str]:
        """Represents a list of possible values for the parameter"""
        return self._possible_values


class Sentence(object):
    """A Sentence consists out of a number of strings and/or parameters. The order in which you
    add the strings/parameters is important!!"""
    def __init__(self):
        self._sentence_parts = []

    def __len__(self):
        return len(self._sentence_parts)

    def __iter__(self):
        index = 0
        while index < len(self._sentence_parts):
            yield self._sentence_parts[index]
            index += 1

    def __getitem__(self, index):
        return self._sentence_parts[index]

    def add_string(self, sentence_part: str):
        """Add a string to the Sentence"""
        self._sentence_parts.append(sentence_part)

    def add_parameter(self, sentence_part: SentenceParameter):
        """Add a parameter to the Sentence"""
        self._sentence_parts.append(sentence_part)


class SentenceBuilder(object):
    def __init__(self):
        self._sentence = Sentence()

    def add_string(self, text: str) -> SentenceBuilder:
        self._sentence.add_string(text)
        return self

    def add_parameter(self, parameter: SentenceParameter) -> SentenceBuilder:
        self._sentence.add_parameter(parameter)
        return self

    def build(self) -> Sentence:
        return self._sentence


class IntentDefinition(object):
    """The IntentDefinition class is a way for IntentHandlers to communicate to other classes how
    the Intents in the IntentHandler can be triggered. An IntentDefinition has a name and one or
    more sentences.

    Example (based on Rhasspy (https://rhasspy.readthedocs.io/en/latest/) syntax):

        intent_definition = IntentDefinition("DimRoom")

        sentence1 = Sentence()
        sentence1.add_string("Dim the lights in the")

        room_parameter = SentenceParameter("Room", True, ["Living Room", "Kitchen", "Garage",
        "Hallway", "Attic", Bedroom"])
        sentence1.add_parameter(room_parameter)

        up_down_parameter = SentenceParameter("UpDown", True, ["Up", "Down"])
        sentence1.add_parameter(up_down_parameter)


        sentence2 = Sentence()

        in_decrease_paramater = SentenceParameter("InDecrease", True, ["Increase", "Decrease"])
        sentence2.add_parameter(in_decrease_parameter)

        sentence2.add_string("the brightness in the")

        sentence2.add_parameter(room_parameter)

        intent_definition.add_sentence(sentence1)
        intent_definition.add_sentence(sentence2)


        For Rhasspy, this IntentDefinition will be converted into:

            [DimRoom]
            Dim the lights in the $Room{Room} (Up | Down){UpDown}
            (Increase | Decrease){InDecrease} the brightness in the $Room{Room}

        """
    def __init__(self, name: str, simple_single_sentence_string: str = None):
        self._name = name
        self._sentences = []
        if simple_single_sentence_string:
            sentence = Sentence()
            sentence.add_string(simple_single_sentence_string)
            self._sentences.append(sentence)

    @property
    def name(self) -> str:
        """Returns the name of the IntentDefinition"""
        return self._name

    def add_sentence(self, sentence: Sentence):
        """Adds a sentence to the collection of sentences within the IntentDefinition"""
        self._sentences.append(sentence)

    @property
    def sentences(self) -> List[Sentence]:
        """Returns the List of sentences inside the IntentDefinition"""
        return self._sentences
