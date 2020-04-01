"""This module provides a static factory that creates an instance of NewIntentSubject"""

from core.newintentsubject import NewIntentSubject
from rhasspy.intentreceiver import RhasspyIntentReceiver


class NewIntentSubjectFactory:
    """Factory that creates a NewIntentSubject object"""

    @staticmethod
    def create_new_intent_subject() -> NewIntentSubject:
        """Creates and returns a NewIntentSubject object"""
        return RhasspyIntentReceiver()
