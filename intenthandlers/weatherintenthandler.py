import configparser
import json
import os
import requests

from core.intentdefinition import IntentDefinition
from core.intenthandler import IntentHandler
from core.intent import Intent


class WeatherIntentHandler(IntentHandler):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        self._api_key = config["Weather"]["openweathermapapikey"]
        self._location = config["Weather"]["location"]
        get_temperature_intent_definition = self._create_intent_definition()
        self._intent_definitions = [get_temperature_intent_definition]

    def _create_intent_definition(self) -> IntentDefinition:
        return self._create_one_string_sentence_intent_definition("GetTemperature", "How (warm | "
                                                                                    "hot | cold) "
                                                                                    "is it")

    def handle_intent(self, intent: Intent) -> str:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s"%
                                self._location,
                                self._api_key)
        content = json.loads(response.content)
        temp = content['main']['temp']
        temp_celsius = int(temp - 273)
        return "At the moment it's {} degrees outside".format(temp_celsius), False
