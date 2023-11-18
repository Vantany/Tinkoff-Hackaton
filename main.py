import requests
import os
from json import loads
from flask import Flask, request
from bot import bestMove
from threading import Thread


class Bot:


    def __init__(self):
        self._session_id = self._get_session_id()
        self._bot_url = self._get_bot_url()
        self._host, self._port = self.get_host_and_port()
        self._mediator_url = self._get_mediator_url()
        self._bot_id = 'resTeam'
        self._bot_password = '(ys#5?e@'
        self._figure = self._registration_request()
        self._logger.send_message(f"BOT_URL: {self._bot_url}", "info")
        self._current_game_field = '_' * 361
        self._thread = None
        self._app = Flask(__name__)

        @self._app.route('/bot/turn', methods=["POST"])
        def make_turn():
            current_game_field = request.json.get("game_field")
            server_response = bestMove(current_game_field, self._figure)
            return {"game_field": server_response}


    def _registration_request(self):


        request_data = {"bot_id": self._bot_id,
                        "password": self._bot_password,
                        "bot_url": self._bot_url}
        extension = f'/sessions/{self._session_id}/registration'
        figure_response = requests.post(self._mediator_url + extension, json=request_data)
        if not figure_response.ok:
            raise requests.RequestException(f'Registration request failed: {figure_response}')
        raw_response = loads(figure_response.content)
        figure = raw_response['figure']
        return figure


    def listen(self):
        print(self._host, int(self._port))
        self._thread = Thread(target=self._app.run, kwargs={'host': self._host, 'port': self._port})
        self._thread.start()



    @staticmethod
    def _get_session_id():
        session_id = os.getenv('SESSION_ID')
        if session_id is None:
            raise ValueError('SESSION_ID is not set')
        return session_id

    @staticmethod
    def _get_bot_url():
        bot_url = os.getenv('BOT_URL')
        if bot_url is None:
            raise ValueError('BOT_URL is not set')
        return bot_url

    def get_host_and_port(self):
        host = self._bot_url.split(':')[1][2:]
        if host is None:
            raise ValueError('HOST is not set')
        port = self._bot_url.split(':')[2]
        if port is None:
            raise ValueError('PORT is not set')
        return host, port

    @staticmethod
    def _get_mediator_url():
        mediator_id = os.getenv('MEDIATOR_URL')
        if mediator_id is None:
            raise ValueError('MEDIATOR_URL is not set')
        return mediator_id
