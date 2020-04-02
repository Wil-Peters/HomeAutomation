import logging
import time

from factories.intenthandlermanagerfactory import IntentHandlerManagerFactory
from factories.newintentsubjectfactory import NewIntentSubjectFactory
from rhasspy.updater import RhasspyUpdater
from speechmanager import SpeechManager


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename='homeautomationserver.log',
                    filemode='w')

if __name__ == "__main__":
    SPEAKER = SpeechManager()
    INTENT_HANDLER_MANAGER = IntentHandlerManagerFactory().create_intent_handler_manager(SPEAKER)
    INTENT_HANDLER_MANAGER.subscribe_intent_handler(SPEAKER)

    UPDATER = RhasspyUpdater(INTENT_HANDLER_MANAGER)
    UPDATER.update_rhasspy()
    UPDATER.train()

    NEW_INTENT_SUBJECT = NewIntentSubjectFactory.create_new_intent_subject()
    NEW_INTENT_SUBJECT.attach(INTENT_HANDLER_MANAGER)

    while True:
        time.sleep(1000)
