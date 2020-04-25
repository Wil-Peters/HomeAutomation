"""This module contains code that makes it possible to automatically update the Sentences & Slots
 of Rhasspy, based on the IntentHandlers which are active in the system"""
import configparser
import json
import logging
import os

from typing import Dict, List

import requests

from core.intentdefinition import IntentDefinition, NumberRangeParameter, SentenceParameter, SetParameter, StringParameter, Variable, VariableParameter
from core.intentdefinitionsource import IntentDefinitionSource
from core.utils.classname import fullname


class RhasspyUpdater:
    """Use this class to automatically train your Rhasspy with a new set of Sentences, based on
    a list of intent defitions.

    To do this, call upload_intent_definitions_to_rhasspy and pass it a List of
    core.intentdefinition.IntentDefinition objects. After that, call the train method."""

    def __init__(self, intent_definition_source: IntentDefinitionSource):
        self._intent_definition_source = intent_definition_source
        self._logger = logging.getLogger(fullname(self))
        self._slots: Dict[str, List[str]] = {}
        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        self._api_url = config["Rhasspy"]["Updater"]

    def _post_slots(self, slots: Dict[str, List[str]]):
        url = self._api_url + "/slots?overwrite_all=true"
        payload = json.dumps(slots)
        self._logger.info(payload)
        response = requests.post(url, payload)
        if response.status_code != 200:
            self._logger.error(response.content)

    def _post_sentences(self, sentences: str):
        url = self._api_url + "/sentences"
        self._logger.info(sentences)
        requests.post(url, sentences)

    def train(self):
        """Triggers the training of Rhasspy. Typically called after
        RhasspyUpdater.upload_intent_definitions_to_rhasspy"""
        url = self._api_url + "/train?nocache=true"
        requests.post(url, None)

    @staticmethod
    def _requires_slot_creation(possible_values: List[str]) -> bool:
        return len(possible_values) > 5

    def update_rhasspy(self):
        """Takes a list of core.intentdefinition.IntentDefinition objects, breaks them down
        into Sentences & Slots and uploads them to Rhasspy"""
        intent_definitions = self._intent_definition_source.get_intent_definitions()
        self._slots = self._get_slots(intent_definitions)
        sentences = self._generate_sentences(intent_definitions)
        if self._slots:
            self._post_slots(self._slots)
        if sentences:
            self._post_sentences(sentences)

    def _get_string_for_variable(self, variable: Variable):
        string = "{} = ".format(variable.name)
        multiple_options = False
        if len(variable.sentences) > 0:
            multiple_options = True
            string += "("
        for sentence in variable.sentences:
            for part in sentence:
                string += self._get_part_string(part)
                if part != sentence[-1]:
                    string += " "
            if sentence != variable.sentences[-1]:
                string += "|"
        if multiple_options:
            string += ")"
        return string

    def _generate_sentences(self, intent_definitions: List[IntentDefinition]):
        sentences = ""
        for intent_definition in intent_definitions:
            if intent_definition.name != "":
                sentences += "[{}]\n".format(intent_definition.name)
                for variable in intent_definition.variables:
                    sentences += self._get_string_for_variable(variable)
                    sentences += "\n"
                if len(intent_definition.variables) > 0:
                    sentences += "\n"
                for sentence in intent_definition.sentences:
                    for part in sentence:
                        sentences += self._get_part_string(part)
                        if part != sentence[-1]:
                            sentences += " "
                    if sentence != intent_definition.sentences[-1]:
                        sentences += "\n"
                if intent_definition != intent_definitions[-1]:
                    sentences += "\n\n"
        return sentences

    def _get_slots(self, intent_definitions: List[IntentDefinition]):
        slots: Dict[str, List[str]] = {}
        for intent_definition in intent_definitions:
            for sentence in intent_definition.sentences:
                for part in sentence:
                    if isinstance(part, SetParameter) and \
                            self._requires_slot_creation(part.possible_values):
                        slot_name, slot_value = self._generate_slot_for_part(slots,
                                                                             intent_definition.name,
                                                                             part)
                        slots[slot_name] = slot_value
            for variable in intent_definition.variables:
                for sentence in variable.sentences:
                    for part in sentence:
                        if isinstance(part, SetParameter) and \
                                self._requires_slot_creation(part.possible_values):
                            slot_name, slot_value = self._generate_slot_for_part(slots,
                                                                                 intent_definition.name,
                                                                                 part)
                            slots[slot_name] = slot_value
        return slots

    @staticmethod
    def _generate_slot_for_part(slots: Dict[str, List[str]], intent_definition_name: str,
                                part: SetParameter):
        slot_name = part.name
        if part.name in slots:
            if slots[part.name] != part.possible_values:
                slot_name = "{}_{}".format(intent_definition_name, part.name)
        return slot_name, part.possible_values

    def _get_part_string(self, part: SetParameter):
        return_value = ""
        if isinstance(part, StringParameter):
            return_value = part.text
            if part.substitute:
                return_value += ":"
            if part.optional:
                return_value = "[{}]".format(return_value)

        if isinstance(part, SetParameter):
            slot_name = part.name
            if self._requires_slot_creation(part.possible_values):
                slot_name = [key for key, values in self._slots.items()
                             if values == part.possible_values][0]
            return_value = self._create_option_string(part, slot_name, part.return_value)
        if isinstance(part, NumberRangeParameter):
            return_value = "({}..{})".format(part.lower_value, part.upper_value)
            return_value += RhasspyUpdater._get_return_value_string_if_necessary(part.return_value,
                                                                                 part)
        if isinstance(part, VariableParameter):
            return_value = "<{}>".format(part.name)
            if part.return_value:
                return_value += " {{{}}}".format(part.name)
        if isinstance(part, SentenceParameter):
            if part.optional:
                return_value = "[{}]".format(return_value)


        return return_value

    @staticmethod
    def _create_option_string(parameter: SetParameter,
                              slot_name: str,
                              add_return_value: bool = False) -> str:
        option_string = ""
        if not RhasspyUpdater._requires_slot_creation(parameter.possible_values):
            option_string += "("
            for i in range(0, len(parameter.possible_values)):
                option_string += parameter.possible_values[i]
                if i != len(parameter.possible_values) - 1:
                    option_string += " | "
            option_string += ")"
        else:
            option_string += "${}".format(slot_name)
        option_string += RhasspyUpdater._get_return_value_string_if_necessary(add_return_value,
                                                                              parameter)
        return option_string

    @staticmethod
    def _get_return_value_string_if_necessary(add_return_value, parameter):
        response = ""
        if add_return_value:
            f = "{{{}}}"
            if isinstance(parameter, NumberRangeParameter):
                f = "{{{}!int}}"
            response = f.format(parameter.name)
        return response
