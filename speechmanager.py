"""This module provides """

from core.intent import Intent
from core.intentdefinition import IntentDefinition, SentenceBuilder, SetParameter
from core.intenthandler import IntentHandler
from core.speaker import Speaker
from rhasspy.speech import RhasspySpeech
from sonos.sonosspeaker import SonosSpeaker


class SpeechManager(Speaker, IntentHandler):

    SPEAKER = "Speaker"
    SONOS = "Sonos"
    RASPBERRY = "Raspberry"
    pi_speaker = RhasspySpeech()
    sonos = SonosSpeaker(pi_speaker)
    current_speaker: Speaker = pi_speaker

    def __init__(self):
        Speaker.__init__(self)
        IntentHandler.__init__(self)
        self._intent_definitions = [self._create_speaker_select_intent_definition()]

    @staticmethod
    def _create_speaker_select_intent_definition():
        intent_definition = IntentDefinition("SelectSpeaker")

        speaker_parameter = SetParameter(SpeechManager.SPEAKER, True,
                                              [SpeechManager.SONOS, SpeechManager.RASPBERRY])

        sentence_builder = SentenceBuilder()
        sentence_builder.add_string("Talk to me on (the)").add_parameter(speaker_parameter)

        sentence = sentence_builder.build()

        intent_definition.add_sentence(sentence)
        return intent_definition

    @staticmethod
    def handle_intent(intent: Intent) -> str:
        if intent.parameters[SpeechManager.SPEAKER] == SpeechManager.RASPBERRY:
            SpeechManager.current_speaker = SpeechManager.pi_speaker
        elif intent.parameters[SpeechManager.SPEAKER] == SpeechManager.SONOS:
            SpeechManager.current_speaker = SpeechManager.sonos
        return "I'm here"

    @staticmethod
    def speak_text(text: str):
        SpeechManager.current_speaker.speak_text(text)
