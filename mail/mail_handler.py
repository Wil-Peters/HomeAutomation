import configparser
from imap_tools import MailBox, Q
import os

from core.intent import Intent
from core.intentdefinition import IntentDefinition
from core.intenthandler import IntentHandler


class MailHandler(IntentHandler):

    _new_mails = []
    _current_email = None

    def __init__(self):
        IntentHandler.__init__(self)
        self._config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        self._config.read(config_file)

        self._intent_definitions = self._create_intent_definitions()

    @staticmethod
    def _create_intent_definitions() -> IntentDefinition:
        get_mails = IntentDefinition("GetEmail", "Do I have [any] (mail|email)")
        email_sender = IntentDefinition("GetEmailSender", "(And the next email|What about the next one|Who is the first (mail|email) from)")
        next_email = IntentDefinition("EmailSubject", "What is the subject")
        read_email = IntentDefinition("ReadEmail", "Can you read (it|the email) to me")

        return [get_mails, email_sender, next_email, read_email]

    def _get_new_emails(self):
        new_emails = []
        for mailbox_name in self._config.sections():
            config = self._config[mailbox_name]
            with MailBox(config["url"]).login(config["address"], config["password"]) as mailbox:
                for msg in mailbox.fetch(Q(seen=False), mark_seen=False):
                    new_emails.append(msg)
        return new_emails

    def handle_intent(self, intent: Intent) -> (str, bool):
        response = ""
        continue_dialog = False
        if intent.name == "GetEmail":
            self._new_mails = self._get_new_emails()
            print(self._new_mails)
            response = "You have {} new messages.".format(len(self._new_mails))
            if len(self._new_mails) > 0:
                continue_dialog = True
        elif intent.name == "GetEmailSender":
            self._current_email = self._new_mails[0]
            response = "It is from {}".format(self._current_email.from_)
            continue_dialog = True
        elif intent.name == "EmailSubject":
            self._current_email = self._new_mails[0]
            response = "The subject of the mail is {}".format(self._current_email.subject)
            continue_dialog = True
        elif intent.name == "ReadEmail":
            if not self._current_email.text:
                response = "Sorry, I cannot read it"
            else:
                response = "{}".format(self._current_email.text)
            if self._current_email != self._new_mails[-1]:
                continue_dialog = True
        return response, continue_dialog
