"""This module provides a static factory that creates an instance of IntentHandlerManager"""

from core.intenthandlermanager import IntentHandlerManager
from core.speaker import Speaker

from intenthandlers.hue.lightsinroomonoffhandler import LightsInRoomOnOffHandler
from intenthandlers.hue.roomdimmer import RoomDimmer
from intenthandlers.timeintenthandler import TimeIntentHandler
from intenthandlers.unknownintenthandler import UnknownIntentHandler
from intenthandlers.weatherintenthandler import WeatherIntentHandler


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
        intent_handler_manager.subscribe_intent_handler(LightsInRoomOnOffHandler())
        intent_handler_manager.subscribe_intent_handler(RoomDimmer())
        intent_handler_manager.subscribe_intent_handler(TimeIntentHandler())
        intent_handler_manager.subscribe_intent_handler(UnknownIntentHandler())
        intent_handler_manager.subscribe_intent_handler(WeatherIntentHandler())

        return intent_handler_manager
