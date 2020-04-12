import json
from unittest import mock, TestCase
from unittest.mock import Mock

from core.intentdefinition import IntentDefinition, NumberRangeParameter, Sentence, SentenceBuilder, SetParameter, Variable
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

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]

        updater = RhasspyUpdater(intent_definition_source_mock)
        updater.update_rhasspy()

        requests_mock.assert_called_once()
        requests_mock.assert_called_with(self.SENTENCES_URL, "[TestIntent]\nSome test text")

    @mock.patch("rhasspy.updater.requests.post")
    def test_optional_string(self, requests_mock):
        requests_mock.return_value.status_code = 200

        sentence = Sentence()
        sentence.add_string("Some test text", True)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]

        updater = RhasspyUpdater(intent_definition_source_mock)
        updater.update_rhasspy()

        requests_mock.assert_called_once()
        requests_mock.assert_called_with(self.SENTENCES_URL, "[TestIntent]\n[Some test text]")

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_string_only_simple_single_sentence(self, requests_mock):
        intent_definition = IntentDefinition("TestIntent", "Some simple test text")

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]

        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        requests_mock.assert_called_with(self.SENTENCES_URL, "[TestIntent]\nSome simple test text")

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_option_string_without_return(self, requests_mock):
        values = ["One", "Two", "Three", "Four", "Five"]
        parameter = SetParameter("Test", possible_values=values)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\n(One | Two | Three | Four | Five)"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intent_in_call)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_parameter_string_without_return(self, requests_mock):
        values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter = SetParameter("Test", possible_values=values)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        updater.update_rhasspy()

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_option_string_with_return(self, requests_mock):
        parameter = SetParameter("Test", True, ["One", "Two", "Three", "Four", "Five"])
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\n(One | Two | Three | Four | Five){Test}"
        requests_mock.assert_has_calls([mock.call(self.SENTENCES_URL, expected_intent_in_call)])

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_parameter_string_with_return(self, requests_mock):
        parameter = SetParameter("Test", True, ["One", "Two", "Three", "Four", "Five", "Six"])
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        updater.update_rhasspy()

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test{Test}")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_create_multiple_parameters(self, requests_mock):
        values1 = ["One", "Two", "Three", "Four", "Five", "Six"]
        values2 = ["One", "Two", "Three", "Four", "Five", "Seven"]

        parameter1 = SetParameter("Test1", True, values1)
        parameter2 = SetParameter("Test2", True, values2)
        sentence = Sentence()
        sentence.add_parameter(parameter1)
        sentence.add_parameter(parameter2)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test1": ["One", "Two", "Three", "Four", "Five", "Six"],
                         "Test2": ["One", "Two", "Three", "Four", "Five", "Seven"]}

        updater.update_rhasspy()

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n$Test1{Test1} $Test2{Test2}")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_one_intent_two_sentence(self, requests_mock):
        sentence = Sentence()
        sentence.add_string("Some test text")

        sentence2 = Sentence()
        sentence2.add_string("Some other test text")
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)
        intent_definition.add_sentence(sentence2)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\nSome test text\nSome other test text"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intent_in_call)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_intents_one_sentence(self, requests_mock):
        sentence = Sentence()
        sentence.add_string("Some test text")

        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        sentence2 = Sentence()
        sentence2.add_string("Some other test text")
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition, intent_definition2]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        expected_intents = "[TestIntent]\nSome test text\n\n[TestIntent2]\nSome other test text"
        requests_mock.assert_called_with(self.SENTENCES_URL, expected_intents)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_slots_same_name_different_values(self, requests_mock):
        values1 = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter1 = SetParameter("Test", True, values1)
        sentence1 = Sentence()
        sentence1.add_parameter(parameter1)
        intent_definition1 = IntentDefinition("TestIntent1")
        intent_definition1.add_sentence(sentence1)

        values2 = ["One", "Two", "Three", "Four", "Five", "Seven"]
        parameter2 = SetParameter("Test", True, values2)
        sentence2 = Sentence()
        sentence2.add_parameter(parameter2)
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition1, intent_definition2]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"],
                         "TestIntent2_Test": ["One", "Two", "Three", "Four", "Five", "Seven"]}

        updater.update_rhasspy()

        expected_intents = "[TestIntent1]\n$Test{Test}\n\n[TestIntent2]\n$TestIntent2_Test{Test}"
        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, expected_intents)]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_two_slots_same_name_same_values(self, requests_mock):
        slot_values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter1 = SetParameter("Test", True, possible_values=slot_values)
        sentence1 = Sentence()
        sentence1.add_parameter(parameter1)
        intent_definition1 = IntentDefinition("TestIntent1")
        intent_definition1.add_sentence(sentence1)

        parameter2 = SetParameter("Test", True, possible_values=slot_values)
        sentence2 = Sentence()
        sentence2.add_parameter(parameter2)
        intent_definition2 = IntentDefinition("TestIntent2")
        intent_definition2.add_sentence(sentence2)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition1, intent_definition2]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        updater.update_rhasspy()

        expected_intents = "[TestIntent1]\n$Test{Test}\n\n[TestIntent2]\n$Test{Test}"
        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, expected_intents)]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_empty_intent_definition(self, requests_mock):
        intent_definition = IntentDefinition("")

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]

        updater = RhasspyUpdater(intent_definition_source_mock)
        updater.update_rhasspy()

        self.assertEqual(0, requests_mock.call_count)

    @mock.patch("rhasspy.updater.requests.post")
    def test_number_range_parameter_without_step(self, requests_mock):
        parameter = NumberRangeParameter("Test", True, -5, 31)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        requests_mock.assert_called_once()
        expected_intent_in_call = "[TestIntent]\n(-5..31){Test!int}"
        requests_mock.assert_has_calls([mock.call(self.SENTENCES_URL, expected_intent_in_call)])

    @mock.patch("rhasspy.updater.requests.post")
    def test_variable(self, requests_mock):
        named_days = ["today", "tomorrow", "the day after tomorrow"]
        weekday_names = ["Monday", "Tuesday", "Wednesday"]
        month_names = ["January", "February", "March", "April", "May", "June"]

        forecast = IntentDefinition("GetWeatherForecast")
        named_days_sentence = SentenceBuilder().add_string("on", True, True) \
            .add_parameter(SetParameter("day", possible_values=named_days + weekday_names))\
            .build()
        date_sentence = SentenceBuilder().add_parameter(NumberRangeParameter("date", lower=0, upper=31)) \
            .add_parameter(SetParameter("month", possible_values=month_names))\
            .build()
        in_days_sentence = SentenceBuilder().add_string("in") \
            .add_parameter(NumberRangeParameter("days", lower=0, upper=7)) \
            .add_string("days")\
            .build()

        day_variable = Variable("day", [named_days_sentence, date_sentence, in_days_sentence])

        forecast.add_variable(day_variable)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [forecast]
        updater = RhasspyUpdater(intent_definition_source_mock)

        updater.update_rhasspy()

        self.assertEqual(2, requests_mock.call_count)
        expected_intent_in_call = "[GetWeatherForecast]\nday = ([on:] $day|(0..31) $month|in (0..7) days)\n\n"
        expected_slots_in_call = """{"day": ["today", "tomorrow", "the day after tomorrow", "Monday", "Tuesday", "Wednesday"], "month": ["January", "February", "March", "April", "May", "June"]}"""
        requests_mock.assert_has_calls([mock.call(self.SLOTS_URL, expected_slots_in_call),
                                        mock.call(self.SENTENCES_URL, expected_intent_in_call)])

    @mock.patch("rhasspy.updater.requests.post")
    def test_optional_parameter_string_without_return(self, requests_mock):
        values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter = SetParameter("Test", possible_values=values, optional=True)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        updater.update_rhasspy()

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n[$Test]")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)

    @mock.patch("rhasspy.updater.requests.post")
    def test_optional_parameter_string_with_return(self, requests_mock):
        values = ["One", "Two", "Three", "Four", "Five", "Six"]
        parameter = SetParameter("Test", return_value=True, possible_values=values, optional=True)
        sentence = Sentence()
        sentence.add_parameter(parameter)
        intent_definition = IntentDefinition("TestIntent")
        intent_definition.add_sentence(sentence)

        intent_definition_source_mock = Mock()
        intent_definition_source_mock.get_intent_definitions.return_value = [intent_definition]
        updater = RhasspyUpdater(intent_definition_source_mock)

        expected_json = {"Test": ["One", "Two", "Three", "Four", "Five", "Six"]}

        updater.update_rhasspy()

        calls = [mock.call(self.SLOTS_URL, json.dumps(expected_json)),
                 mock.call(self.SENTENCES_URL, "[TestIntent]\n[$Test{Test}]")]
        self.assertEqual(2, requests_mock.call_count)
        requests_mock.assert_has_calls(calls)