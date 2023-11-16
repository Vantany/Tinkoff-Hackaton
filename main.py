from flask import Flask, request, jsonify
import os
import requests
from bot import bestMove
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
str_grid = "_"*361
figure = None

BOT_URL = os.getenv("BOT_URL")
BOT_ID = os.getenv("BOT_ID")
PASSWORD = os.getenv("PASSWORD")

MEDIATOR_URL = os.getenv("MEDIATOR_URL")
SESSION_ID = os.getenv("SESSION_ID")


def registerBotInSessionResponse():
    global bot_id, password
    mediator_url = os.getenv("MEDIATOR_URL")
    session_id = os.getenv("SESSION_ID")
    bot_url = os.getenv("BOT_URL")
    requests.post(f"{mediator_url}/sessions/{session_id}/registration",
                  {"bot_id": bot_id, "password": password, "bot_url": bot_url})


def registerBotInSessionRequest():
    mediator_url = os.getenv("MEDIATOR_URL")
    session_id = os.getenv("SESSION_ID")
    return requests.get(f"{mediator_url}/sessions/{session_id}/registration").json()["figure"]


@app.route("/bot/turn", methods = ["POST", "GET"])
def botTurnHandler():
    global str_grid, figure
    if request.method == "POST":
        str_grid = request.form["game_field"]
        str_grid = bestMove(str_grid=str_grid, curFig=figure)
    else:
        return jsonify({"game_field" : str_grid})
        

if __name__ == '__main__':
    app.run(host= BOT_URL)
    registerBotInSessionResponce()
    figure = registerBotInSessionRequest()
