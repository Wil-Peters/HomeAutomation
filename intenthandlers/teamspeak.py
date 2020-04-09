import subprocess
from core.intent import Intent
from core.intentdefinition import IntentDefinition, Sentence, SetParameter
from core.intenthandler import IntentHandler


class TeamspeakIntentHandler(IntentHandler):

    ACTION = "Action"
    COMMAND = "/home/wil/teamspeak3-server_linux_amd64/ts3server_startscript.sh {}"

    def __init__(self):
        super().__init__()
        room_on_off_intent_definition = self._create_intent_definition()
        self._intent_definitions = [room_on_off_intent_definition]

    @staticmethod
    def _create_intent_definition() -> IntentDefinition:
        start_stop_server_definition = IntentDefinition("StartStopTeamspeakServer")
        sentence = Sentence()
        sentence.add_parameter(SetParameter(TeamspeakIntentHandler.ACTION,
                                                 True,
                                                 possible_values=["Start", "Stop"]))
        sentence.add_string("teamspeak server")
        start_stop_server_definition.add_sentence(sentence)
        return start_stop_server_definition

    @staticmethod
    def _create_response_string(action: str):
        response = "{} the teamspeak server"
        if action.lower() == "start":
            response.format("Starting")
        else:
            response.format("Stopping")
        return response

    @staticmethod
    def handle_intent(intent: Intent) -> str:
        action = intent.parameters[TeamspeakIntentHandler.ACTION]
        start_stop_server_bash_command = TeamspeakIntentHandler.COMMAND.format(action.lower())
        process = subprocess.Popen(start_stop_server_bash_command.split(), stdout=subprocess.PIPE)
        process.communicate()
        return TeamspeakIntentHandler._create_response_string(action)
