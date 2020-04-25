"""This module provides a static factory that creates an instance of IntentHandlerManager"""
from typing import List

from core.asynchronous import AsyncVoiceSource
from core.intenthandler import IntentHandler
from core.intenthandlermanager import IntentHandlerManager
from core.triggermanager import TriggerManager
from core.speaker import Speaker

from intenthandlers.hue.lightsinroomonoffhandler import LightsInRoomOnOffHandler
from intenthandlers.hue.roomdimmer import RoomDimmer
from intenthandlers.teamspeak import TeamspeakIntentHandler
from intenthandlers.timeintenthandler import TimeIntentHandler
from intenthandlers.timerintenthandler import TimerIntenthandler
from intenthandlers.weatherintenthandler import WeatherIntentHandler

from mail.mail_handler import MailHandler


class IntentHandlerManagerFactory(object):
    """Factory that creates an IntentHandlerManager object"""

    def __init__(self):
        pass

    @staticmethod
    def create_intent_handler_manager(speaker: Speaker):
        """- Creates an IntentHandlerManager object
        - Creates an instance of each class implementing the IntentHandler Abstract Base class
        - Subscribes every IntentHandler instance to the IntentHandlerManager
        """
        intent_handler_manager = IntentHandlerManager(speaker)
        intent_handlers: List[IntentHandler] = [LightsInRoomOnOffHandler(),
                                                RoomDimmer(),
                                                TeamspeakIntentHandler(),
                                                TimeIntentHandler(),
                                                WeatherIntentHandler(),
                                                MailHandler()
                                                ]

        async_voice_sources : List[AsyncVoiceSource] = []

        timer_intent_handler = TimerIntenthandler()
        intent_handlers.append(timer_intent_handler)
        async_voice_sources.append(timer_intent_handler)

        for intent_handler in intent_handlers:
            intent_handler_manager.subscribe_intent_handler(intent_handler)

        trigger_manager = TriggerManager(speaker)

        for async_voice_source in async_voice_sources:
            async_voice_source.subscribe(trigger_manager)

        return intent_handler_manager
