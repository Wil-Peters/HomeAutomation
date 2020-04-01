"""This module sets up a server which hosts wav files, which can then be played by a Sonos
speaker"""
import http.server
import logging
import os
import socket
import socketserver

from typing import ByteString


class SpeechFileServer(object):
    """
    This class does 2 things:
        - It sets up a file server.
        - It stores byte strings as wav files on the server.
    """
    _port = 8000
    _address = ""
    _logger = logging.getLogger(__name__)

    def host_as_wav_file_and_return_url(self, speech_bytes: ByteString) -> str:
        """This method takes a ByteString as a parameter and save that ByteString as a wav file
        on the server. The url at which the file can be reached is returned."""
        filename = "speech.wav"
        with open(filename, "wb") as wav_file:
            wav_file.write(bytearray(speech_bytes))
        return "http://" + self._address + "/" + filename

    def start_server(self):
        """Starts the server. Call from a new Thread, as this is a blocking method, and it will
        never return"""
        handler = http.server.SimpleHTTPRequestHandler
        handler.extensions_map.update({'.webapp': 'application/x-web-app-manifest+json'})

        folder_name = "speech_files"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        os.chdir(folder_name)
        httpd = socketserver.TCPServer(("", self._port), handler)

        self._address = socket.gethostbyname(socket.gethostname()) + ":%s" % self._port

        self._logger.info("Serving speech files at: %s", self._address)
        httpd.serve_forever()
