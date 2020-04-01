from abc import ABC, abstractmethod

from core.newintentobserver import NewIntentObserver


class NewIntentSubject(ABC):
    """The NewIntentObserver & NewIntentSubject abstract base classes are used to have a clean
    interface between the part of the code where the origin of the Intent lies, and the part
    where the Intent is handled."""
    @abstractmethod
    def attach(self, observer: NewIntentObserver) -> None:
        """
        Attach a NewIntentObserver to the NewIntentSubject.
        """
        pass

    @abstractmethod
    def detach(self, observer: NewIntentObserver) -> None:
        """
        Detach a NewIntentObserver from the NewIntentSubject.
        """
        pass
