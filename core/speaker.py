from abc import ABC


class Speaker(ABC):
    """Defines an abstract base class for any kind of speaker that can translate a text string
    into a voice response."""
    def __init__(self):
        pass

    def speak_text(self, text):
        pass
