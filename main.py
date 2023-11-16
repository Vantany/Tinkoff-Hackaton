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
    global BOT_URL, BOT_ID, PASSWORD, MEDIATOR_URL, SESSION_ID
    requests.post(f"{MEDIATOR_URL}/sessions/{SESSION_ID}/registration",
                  {"bot_id": BOT_ID, "password": PASSWORD, "bot_url": BOT_URL})


def registerBotInSessionRequest():
    global MEDIATOR_URL, SESSION_ID
    return requests.get(f"{MEDIATOR_URL}/sessions/{SESSION_ID}/registration").json()["figure"]


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
