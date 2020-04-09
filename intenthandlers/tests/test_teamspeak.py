from unittest import TestCase

from intenthandlers.teamspeak import TeamspeakIntentHandler


class TestStartStopTeamspeakServerIntentHandler(TestCase):
    def test_get_intent_definitions(self):
        teamspeak_server_intent_handler = TeamspeakIntentHandler()
        intent_definitions = teamspeak_server_intent_handler.intent_definitions

        self.assertEqual(1, len(intent_definitions))

        sentences = intent_definitions[0].sentences
        self.assertEqual(1, len(sentences))
        self.assertEqual(2, len(sentences[0]))
        parameter = sentences[0][0]
        self.assertIsNotNone(parameter)
        self.assertTrue(parameter.return_value)
        self.assertEqual(2, len(parameter.possible_values))
