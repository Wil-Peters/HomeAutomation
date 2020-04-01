import configparser
import os

from typing import ByteString

import requests

from core.speaker import Speaker
from core.texttospeech import TextToSpeechGenerator


class RhasspySpeech(Speaker, TextToSpeechGenerator):

    def __init__(self):
        Speaker.__init__(self)
        TextToSpeechGenerator.__init__(self)
        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        self._api_url = config["Rhasspy"]["Speaker"]

    def speak_text(self, text: str):
        requests.post(self._api_url + "/text-to-speech", text)

    def generate_speech_file(self, text: str) -> ByteString:
        return requests.post(self._api_url + "/text-to-speech?play=false", text).content
