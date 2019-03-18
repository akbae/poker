from flask import Flask, request
import json
import uuid

from models.poker import Poker
from models.state import State

app = Flask(__name__)
poker = Poker()


@app.route("/state", methods=["GET"])
def state():
    return json.dumps(State.to_dict(poker.state))


@app.route("/add-player", methods=["POST"])
def add_player():
    request_json = request.get_json(force=True)
    name = request_json["name"]
    return str(poker.add_player(name))


@app.route("/buy-in", methods=["POST"])
def buy_in():
    request_json = request.get_json(force=True)
    player_uuid = uuid.UUID(request_json["player_uuid"])
    amount = int(request_json["amount"])
    poker.buy_in(player_uuid, amount)
    return json.dumps(State.to_dict(poker.state))


@app.route("/start-game", methods=["POST"])
def start_game():
    poker.start_game()
    return json.dumps(State.to_dict(poker.state))


@app.route("/check", methods=["POST"])
def check():
    request_json = request.get_json(force=True)
    player_uuid = uuid.UUID(request_json["player_uuid"])
    poker.check(player_uuid)
    return json.dumps(State.to_dict(poker.state))


@app.route("/bet", methods=["POST"])
def bet():
    request_json = request.get_json(force=True)
    player_uuid = uuid.UUID(request_json["player_uuid"])
    amount = int(request_json["amount"])
    poker.bet(player_uuid, amount)
    return json.dumps(State.to_dict(poker.state))


@app.route("/fold", methods=["POST"])
def fold():
    request_json = request.get_json(force=True)
    player_uuid = uuid.UUID(request_json["player_uuid"])
    poker.fold(player_uuid)
    return json.dumps(State.to_dict(poker.state))


@app.route("/cash-out", methods=["POST"])
def cash_out():
    request_json = request.get_json(force=True)
    player_uuid = uuid.UUID(request_json["player_uuid"])
    return poker.cash_out(player_uuid)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
