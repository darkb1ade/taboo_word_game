from flask import Flask, Request, Response, request, jsonify
from src import Engine
import logging

# logger = logging.getLogger(__name__)
app = Flask(__name__, static_url_path="")
app.config["DEBUG"] = True
ENGINE = Engine()


@app.route("/init_engine", methods=["GET"])
def init_engine():
    names = request.args.get("names").replace(" ", "")
    names = names.split(",")

    avatars = request.args.get("avatars")
    if avatars is not None:
        avatars = request.args.get("avatars").replace(" ", "")
        avatars = avatars.split(",")

    app.logger.info(f"start /init_engine {names=} {avatars=}")
    ENGINE.init_engine(names=names, avatar_list=avatars)
    app.logger.info(ENGINE)
    return "ok"


@app.route("/add", methods=["GET"])
def add():
    app.logger.info(ENGINE)
    word = request.args.get("word")

    app.logger.info(f"start /add {word=} {word=}")
    msg = ENGINE.add(word)

    return msg


@app.route("/random", methods=["GET"])
def random():
    app.logger.info(f"start /random")

    msg = ENGINE.run()
    players = [{"name": player.name, "url": player.url} for player in ENGINE.players]
    app.logger.info(f"start /random msg={msg}, player={players}")
    return jsonify({"player": players, "message": msg})


if __name__ == "__main__":
    app.run(debug=True)
