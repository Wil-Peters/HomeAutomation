from unittest import TestCase

from core.intent import Intent


class TestIntent(TestCase):

    def test___init__(self):
        test_name = "TestIntentName"
        test_parameters = {"TestParameter1": "Value1", "TestParameter2": "Value3"}
        intent = Intent(test_name, "Test", test_parameters)
        self.assertEqual(test_name, intent.name)
        self.assertEqual(test_parameters, intent.parameters)
