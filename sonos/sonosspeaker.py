import configparser
import os
import threading

import soco  # type: ignore

from sonos.server import SpeechFileServer
from core.speaker import Speaker
from core.texttospeech import TextToSpeechGenerator


class SonosSpeaker(Speaker):

    def __init__(self, text_to_speech_generator: TextToSpeechGenerator):
        Speaker.__init__(self)
        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        self._server = SpeechFileServer()
        thread = threading.Thread(target=self._server.start_server, daemon=True)
        thread.start()
        for zone in soco.discover():
            if zone.player_name == config["Sonos"]["Speaker"]:
                self._speaker = zone
        self._speech_generator = text_to_speech_generator

    def speak_text(self, text):
        byte_string = self._speech_generator.generate_speech_file(text)
        url = self._server.host_as_wav_file_and_return_url(byte_string)
        self._speaker.play_uri(url)
