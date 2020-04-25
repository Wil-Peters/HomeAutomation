import threading

from core.asynchronous import AsyncVoiceSource, Reminder
from core.intent import Intent
from core.intentdefinition import IntentDefinition, NumberRangeParameter, SentenceBuilder, \
    SetParameter
from core.intenthandler import IntentHandler


class TimerIntenthandler(AsyncVoiceSource, IntentHandler):

    TIMEUNIT = "TimeUnit"
    AMOUNT = "Amount"
    SECONDS = "seconds"
    MINUTES = "minutes"

    def __init__(self):
        AsyncVoiceSource.__init__(self)
        IntentHandler.__init__(self)

        get_time_intent_definition = self._create_get_time_intent_definition()
        self._intent_definitions = [get_time_intent_definition]

    def _create_get_time_intent_definition(self) -> IntentDefinition:
        set_timer = IntentDefinition("SetTimer")

        numbers_parameter = NumberRangeParameter(self.AMOUNT, True, lower=0, upper=60)
        time_unit_parameter = SetParameter(self.TIMEUNIT, True, possible_values=[self.SECONDS,
                                                                                 self.MINUTES])

        sentence_builder = SentenceBuilder()
        sentence_builder.add_string("Set a timer for") \
            .add_parameter(numbers_parameter) \
            .add_parameter(time_unit_parameter) \
            .add_string("from now", True)

        sentence = sentence_builder.build()
        set_timer.add_sentence(sentence)
        return set_timer

    def _timer_expired(self):
        self._listener.trigger(Reminder("Timer expired"))

    def handle_intent(self, intent: Intent) -> str:
        seconds = 0
        if intent.parameters[self.TIMEUNIT] == self.SECONDS:
            seconds = int(intent.parameters[self.AMOUNT])
        elif intent.parameters[self.TIMEUNIT] == self.MINUTES:
            seconds = int(intent.parameters[self.AMOUNT]) * 60
        timer = threading.Timer(seconds, self._timer_expired)
        timer.start()
        return "I've set a timer for {} seconds from now".format(seconds), False
