from unittest import TestCase
from unittest.mock import MagicMock, Mock

from core.asynchronous import Notification, Reminder
from core.intent import Intent
from core.triggermanager import TriggerManager


class TestTriggerManager(TestCase):
    def test_hold_and_resume_notifications(self):
        speaker = Mock()
        speaker.speak_text = MagicMock()
        trigger_manager = TriggerManager(speaker)

        hold_notification_intent = Intent("HoldNotifications", "Hold all notifications", {})
        trigger_manager.handle_intent(hold_notification_intent)

        notification = Notification("Notification test")
        trigger_manager.trigger(notification)

        speaker.speak_text.assert_not_called()

        resume_notification_intent = Intent("ResumeNotifications", "Resume all notifications", {})
        trigger_manager.handle_intent(resume_notification_intent)

        notification2 = Notification("Notification test 2")
        trigger_manager.trigger(notification2)

        speaker.speak_text.assert_called_once()

    def test_get_number_of_notifications(self):
        speaker = Mock()
        speaker.speak_text = MagicMock()
        trigger_manager = TriggerManager(speaker)

        hold_notification_intent = Intent("HoldNotifications", "Hold all notifications", {})
        trigger_manager.handle_intent(hold_notification_intent)

        notification = Notification("Notification test")
        trigger_manager.trigger(notification)

        notification2 = Notification("Notification test 2")
        trigger_manager.trigger(notification2)

        speaker.speak_text.assert_not_called()
        response = trigger_manager.handle_intent(Intent("GetNumberOfNotifications", "Test", {}))
        self.assertEqual("There are 2 notifications in the queue", response)

    def test_reminder(self):
        speaker = Mock()
        speaker.speak_text = MagicMock()
        trigger_manager = TriggerManager(speaker)

        reminder = Reminder("Reminder test")
        trigger_manager.trigger(reminder)

        speaker.speak_text.assert_called_with("Reminder test")

    def test_notification(self):
        speaker = Mock()
        speaker.speak_text = MagicMock()
        trigger_manager = TriggerManager(speaker)

        notification = Notification("Notification test")
        trigger_manager.trigger(notification)

        speaker.speak_text.assert_called_with("Notification test")

    def test_first_notification(self):
        speaker = Mock()
        speaker.speak_text = MagicMock()
        trigger_manager = TriggerManager(speaker)

        hold_notification_intent = Intent("HoldNotifications", "Hold all notifications", {})
        trigger_manager.handle_intent(hold_notification_intent)

        notification = Notification("Notification test 1")
        trigger_manager.trigger(notification)

        notification2 = Notification("Notification test 2")
        trigger_manager.trigger(notification2)

        speaker.speak_text.assert_not_called()
        response = trigger_manager.handle_intent(Intent("GetFirstNotification", "Test", {}))
        self.assertEqual("Notification test 1", response)

        response = trigger_manager.handle_intent(Intent("GetNumberOfNotifications", "Test", {}))
        self.assertEqual("There are 1 notifications in the queue", response)
