from abc import ABC, abstractmethod

from core.intent import Intent


class NewIntentObserver(ABC):
    """The NewIntentObserver & NewIntentSubject abstract base classes are used to have a clean
    interface between the part of the code where the origin of the Intent lies, and the part
    where the Intent is handled."""
    @abstractmethod
    def update(self, intent: Intent) -> None:
        pass
