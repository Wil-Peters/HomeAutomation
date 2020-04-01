from unittest import TestCase

from intenthandlers.weatherintenthandler import WeatherIntentHandler


class TestWeatherIntentHandler(TestCase):
    def test_get_intent_definitions(self):
        weather_intent_handler = WeatherIntentHandler()
        intent_definitions = weather_intent_handler.intent_definitions

        self.assertEqual(1, len(intent_definitions))

        sentences = intent_definitions[0].sentences
        self.assertEqual(1, len(sentences))
        self.assertEqual(1, len(sentences[0]))
        self.assertEqual("How (warm | hot | cold) is it", sentences[0][0])
