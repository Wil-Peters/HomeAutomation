import json
from unittest import mock, TestCase

from core.intentdefinition import IntentDefinition, Sentence, SentenceParameter
from rhasspy.updater import RhasspyUpdater


class TestRhasspyUpdater(TestCase):

    SENTENCES_URL = "http://192.168.1.13:12101/api/sentences"
    SLOTS_URL = "http://192.168.1.13:12101/api/slots?overwrite_all=true"

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_string_only(self, requests_mock):
        requests_mock.return_value.status_code = 200

        sentence = Sentence()
        sentence.add_string("Some test text")
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater = RhasspyUpdater()
        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        requests_mock.assert_called_once()
        requests_mock.assert_called_with(self.SENTENCES_URL, "[TestIntent]\nSome test text")

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_string_only_simple_single_sentence(self, requests_mock):
        updater = RhasspyUpdater()

        intent_definition = IntentDefinition("TestIntent", "Some simple test text")

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        requests_mock.assert_called_once()
        requests_mock.assert_called_with(self.SENTENCES_URL, "[TestIntent]\nSome simple test text")

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_option_string_without_return(self, requests_mock):
        updater = RhasspyUpdater()

        values = ["One", "Two", "Three", "Four", "Five"]
        parameter = SentenceParameter("Test", possible_values=values)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\n(One | Two | Three | Four | Five)"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intent_in_call)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_parameter_string_without_return(self, requests_mock):
        updater = RhasspyUpdater()

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter = SentenceParameter("Test", possible_values=values)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_option_string_with_return(self, requests_mock):
        updater = RhasspyUpdater()

        parameter = SentenceParameter("Test", True, ["One", "Two", "Three", "Four", "Five"])
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\n(One | Two | Three | Four | Five){Test}"
        requests_mock.assert_has_calls([mock.call(self.SENTENCES_URL, expected_intent_in_call)])

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_parameter_string_with_return(self, requests_mock):
        updater = RhasspyUpdater()

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        parameter = SentenceParameter("Test", True, ["One", "Two", "Three", "Four", "Five", "Six"])
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test{Test}")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_multiple_parameters(self, requests_mock):
        updater = RhasspyUpdater()

        expected_json = {"Test1": ["One", "Two", "Three", "Four", "Five", "Six"],
                         "Test2": ["One", "Two", "Three", "Four", "Five", "Seven"]}

        values1 = ["One", "Two", "Three", "Four", "Five", "Six"]
        values2 = ["One", "Two", "Three", "Four", "Five", "Seven"]

        parameter1 = SentenceParameter("Test1", True, values1)
        parameter2 = SentenceParameter("Test2", True, values2)
        sentence = Sentence()
        sentence.add_parameter(parameter1)
        sentence.add_parameter(parameter2)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test1{Test1} $Test2{Test2}")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_one_intent_two_sentence(self, requests_mock):
        updater = RhasspyUpdater()

        sentence = Sentence()
        sentence.add_string("Some test text")

        sentence2 = Sentence()
        sentence2.add_string("Some other test text")
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)
        intent_definition.add_sentence(sentence2)

        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\nSome test text\nSome other test text"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intent_in_call)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_intents_one_sentence(self, requests_mock):
        updater = RhasspyUpdater()

        sentence = Sentence()
        sentence.add_string("Some test text")

        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        sentence2 = Sentence()
        sentence2.add_string("Some other test text")
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        updater.upload_intent_definitions_to_rhasspy([intent_definition, intent_definition2])

        requests_mock.assert_called_once()
        expected_intents = "[TestIntent]\nSome test text\n\n[TestIntent2]\nSome other test text"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intents)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_slots_same_name_different_values(self, requests_mock):
        updater = RhasspyUpdater()

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"],
                         "TestIntent2_Test": ["One", "Two", "Three", "Four", "Five", "Seven"]}

        values1 = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter1 = SentenceParameter("Test", True, values1)
        sentence1 = Sentence()
        sentence1.add_parameter(parameter1)
        intent_definition1 = IntentDefinition("TestIntent1")
        intent_definition1.add_sentence(sentence1)

        values2 = ["One", "Two", "Three", "Four", "Five", "Seven"]
        parameter2 = SentenceParameter("Test", True, values2)
        sentence2 = Sentence()
        sentence2.add_parameter(parameter2)
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        updater.upload_intent_definitions_to_rhasspy([intent_definition1, intent_definition2])

        expected_intents = "[TestIntent1]\n$Test{Test}\n\n[TestIntent2]\n$TestIntent2_Test{Test}"
        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, expected_intents)]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_slots_same_name_same_values(self, requests_mock):
        updater = RhasspyUpdater()

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        slot_values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter1 = SentenceParameter("Test", True, possible_values=slot_values)
        sentence1 = Sentence()
        sentence1.add_parameter(parameter1)
        intent_definition1 = IntentDefinition("TestIntent1")
        intent_definition1.add_sentence(sentence1)

        parameter2 = SentenceParameter("Test", True, possible_values=slot_values)
        sentence2 = Sentence()
        sentence2.add_parameter(parameter2)
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        updater.upload_intent_definitions_to_rhasspy([intent_definition1, intent_definition2])

        expected_intents = "[TestIntent1]\n$Test{Test}\n\n[TestIntent2]\n$Test{Test}"
        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, expected_intents)]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_empty_intent_definition(self, requests_mock):
        intent_definition = IntentDefinition("")

        updater = RhasspyUpdater()
        updater.upload_intent_definitions_to_rhasspy([intent_definition])

        self.assertEqual(0, requests_mock.call_count)
