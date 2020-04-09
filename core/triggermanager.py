from typing import List

from core.asynchronous import Trigger, Notification, AsyncVoiceListener
from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intenthandler import IntentHandler
from core.speaker import Speaker


class TriggerManager(AsyncVoiceListener, IntentHandler):

    def __init__(self, speaker: Speaker):
        AsyncVoiceListener.__init__(self)
        self._speaker: Speaker = speaker
        self._intent_definitions = self.create_intent_definitions()
        self._notifications: List[Trigger] = []
        self._hold_notifications = False

    def trigger(self, trigger: Trigger):
        if self._hold_notifications and isinstance(trigger, Notification):
            self._notifications.append(trigger)
        else:
            if self._speaker:
                self._speaker.speak_text(trigger.message)

    def create_intent_definitions(self) -> List[IntentDefinition]:
        hold_notifications = IntentDefinition("HoldNotifications", "Block notifications")
        resume_notifications = IntentDefinition("ResumeNotifications", "Resume notifications")
        get_number_of_notifications = IntentDefinition("GetNumberOfNotifications",
                                                       "How many notifications are in the queue")
        first_notification = IntentDefinition("GetFirstNotification",
                                              "Tell me the first notification")
        return [hold_notifications,
                resume_notifications,
                get_number_of_notifications,
                first_notification]

    def handle_intent(self, intent: Intent) -> str:
        if intent.name == "HoldNotifications":
            self._hold_notifications = True
            return "Holding all notifications"
        elif intent.name == "ResumeNotifications":
            self._hold_notifications = False
            return "Resuming all notifications"
        elif intent.name == "GetNumberOfNotifications":
            return "There are {} notifications in the queue".format(len(self._notifications))
        elif intent.name == "GetFirstNotification":
            return self._notifications.pop(0).message
        raise Exception("Don't know how to handle an intent of type {}".format(intent.name))
