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


@app.route(f"{MEDIATOR_URL}/sessions/{SESSION_ID}/registration", methods = ["POST", "GET"])
def botRegistrationHandler():
    global figure
    if request.method == "POST":
        figure = request.form["figure"]
    else:
        return jsonify({"bot_id": BOT_ID, "password": PASSWORD, "bot_url": BOT_URL})


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