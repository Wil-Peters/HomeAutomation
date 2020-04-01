from abc import ABC
from typing import ByteString


class TextToSpeechGenerator(ABC):
    """Defines an abstract base class for any class that can convert a text string into a
    ByteString."""
    def __init(self):
        pass

    def generate_speech_file(self, text: str) -> ByteString:
        pass
