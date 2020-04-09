from abc import ABC


class Trigger(ABC):

    def __init__(self, text: str):
        self._text = text

    @property
    def message(self) -> str:
        return self._text


class Reminder(Trigger):
    def __init__(self, text: str):
        Trigger.__init__(self, text)


class Notification(Trigger):
    def __init__(self, text: str):
        Trigger.__init__(self, text)


class AsyncVoiceListener(ABC):

    def __init__(self):
        pass

    def trigger(self, trigger: Trigger):
        pass


class AsyncVoiceSource(ABC):

    _listener = None

    def __init__(self):
        pass

    def subscribe(self, listener: AsyncVoiceListener):
        self._listener = listener
