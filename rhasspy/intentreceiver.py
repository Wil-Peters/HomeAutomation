"""Module that handles intents coming from Rhasspy. Rhasspy intents are converted to
core.intent.Intent objects and then passed to any NewIntentObservers which are listening"""
import configparser
import json
import logging
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from threading import Thread

import requests

from core.intent import Intent
from core.newintentobserver import NewIntentObserver
from core.newintentsubject import NewIntentSubject
from core.utils.classname import fullname


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Objects of SimpleHTTPRequestHandler are constructed by the HTTPServer when a POST message
    is received. Handles the POST and returns a response to Rhasspy."""

    def do_POST(self):
        """
        Handles POST messages to the HTTPServer. Expects intent json in the style of Rhasspy
        :return:
        """
        content_length = int(self.headers['Content-Length'])
        intent_string = self.rfile.read(content_length)
        response_string = RhasspyIntentReceiver().handle_new_intent(intent_string)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(response_string.encode("utf-8"))
        self.wfile.write(response.getvalue())


class RhasspyIntentReceiver(NewIntentSubject):
    """Contains functionality to convert Rhasspy intent json into core.intent.Intent objects.
    Also constructs the response for the POST message, back to Rhasspy"""

    HOST = ''
    PORT = 8081
    _intent_listener = None
    _timer = None
    api_url = None

    def __init__(self):
        self._logger = logging.getLogger(fullname(self))
        thread = Thread(target=self._run_server, daemon=True)
        thread.start()

        conversation_mode_thread = Thread(target=self._start_conversation_mode, daemon=True)
        conversation_mode_thread.start()

        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        RhasspyIntentReceiver.api_url = config["Rhasspy"]["Speaker"]

    def _start_conversation_mode(self):
        RhasspyIntentReceiver._intent_handled = False
        while True:
            time.sleep(1)
            if RhasspyIntentReceiver._intent_handled:
                RhasspyIntentReceiver._intent_handled = False
                requests.post(RhasspyIntentReceiver.api_url + "/listen-for-command")

    def handle_new_intent(self, intent_string: str):
        """Typically called from the SimpleHTTPRequestHandler.do_POST method, this method takes
        raw json, converts it into an object of type core.intent.Intent and notifies any
        NewIntentObservers of the arrival of the new Intent.
        Returns a string containing the response body which is to be returned to Rhasspy"""
        incoming_time = time.time()
        self._logger.info("Received intent: %s", intent_string)
        intent = self._create_intent_object(intent_string)
        response = ""
        if intent.name != "" and intent.full_intent_string != "":
            if RhasspyIntentReceiver._intent_listener:
                response, continue_dialog = RhasspyIntentReceiver._intent_listener.update(intent)
                if continue_dialog:
                    RhasspyIntentReceiver._intent_handled = True
        self._logger.info("Response: {}".format(response))
        return self._create_return_body(intent, incoming_time, response)

    def attach(self, observer: NewIntentObserver):
        """Attaches a new observer which implements the core.newintentobserver.NewIntentObserver
        class"""
        self._logger.info("Attached observer: %s", observer)
        RhasspyIntentReceiver._intent_listener = observer

    def detach(self, observer: NewIntentObserver):
        """Detaches an observer which implements the core.newintentobserver.NewIntentObserver
        class"""
        self._logger.info("Detached observer: %s", observer)
        RhasspyIntentReceiver._intent_listener = None

    def _run_server(self):
        httpd = HTTPServer((self.HOST, self.PORT), SimpleHTTPRequestHandler)
        httpd.serve_forever()

    @staticmethod
    def _create_intent_object(raw_intent_string: str):
        intent_dict = json.loads(raw_intent_string)
        name = intent_dict["intent"]["name"]
        if "slots" in intent_dict:
            return Intent(name, intent_dict["text"], intent_dict["slots"])
        return Intent(name, intent_dict["text"])

    @staticmethod
    def _create_return_body(intent: Intent, timestamp: float, response: str):
        response_dict = {"intent": intent.name, "time_sec": round(time.time() - timestamp, 2),
                         "response": response}
        return json.dumps(response_dict)
