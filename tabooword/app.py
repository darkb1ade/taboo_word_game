from flask import Flask, Request, Response, request, jsonify
from src import Engine
import logging

# logger = logging.getLogger(__name__)
app = Flask(__name__, static_url_path="")
app.config["DEBUG"] = True
ENGINE = Engine()


@app.route(
    "/init_engine", methods=["POST"]
)  # init player & avatar (exclude randomizer)
def init_engine():
    # 1. set names
    names = request.args.get("names").replace(" ", "")
    names = names.split(",")
    # 2. set avatars
    avatars = request.args.get("avatars")
    if avatars is not None:
        avatars = request.args.get("avatars").replace(" ", "")
        avatars = avatars.split(",")
    # 3. reset words
    is_reset_words = bool(request.args.get("words"))

    app.logger.info(f"start /init_engine {names=} {avatars=} {is_reset_words=}")
    if is_reset_words is True:
        ENGINE.reset()
        app.logger.info(f"start /init_engine reset_word")

    ENGINE.init_engine(names=names, avatar_list=avatars)
    app.logger.info(ENGINE)
    return "ok"


@app.route("/reset_word", methods=["POST"])  # reset word inside randomizer
def reset():
    app.logger.info(f"start /reset_word")
    ENGINE.reset()
    app.logger.info(ENGINE)
    return "OK"


@app.route("/add", methods=["POST"])  # add word to the randomizer
def add():
    word = request.args.get("word")
    app.logger.info(f"start /add {word=}")
    try:
        msg = ENGINE.add(word)
        app.logger.info(ENGINE)
        return Response(msg, status=200, mimetype="application/json")

    except AssertionError as e:  # duplicated word
        app.logger.info(e)
        return Response(e.args[0], status=404, mimetype="application/json")


@app.route("/random", methods=["POST"])
def random():
    app.logger.info(f"start /random")
    try:
        msg = ENGINE.run()
        players = [
            {"name": player.name, "url": player.url} for player in ENGINE.players
        ]
        app.logger.info(f"start /random {msg=}, {players=}")
        app.logger.info(ENGINE)
        return jsonify({"player": players, "message": msg})

    except AssertionError as e:  # word not enough or engine not init
        app.logger.info(e)
        return Response(e.args[0], status=404, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
