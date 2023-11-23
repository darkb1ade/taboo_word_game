from flask import Flask, Request, Response, request, jsonify
from src import Engine
import logging
from flask_cors import CORS

app = Flask(__name__, static_url_path="")
app.config["DEBUG"] = True
ENGINE = Engine()
CORS(app)


@app.route(
    "/init_engine", methods=["POST"]
)  # init player & avatar (exclude randomizer)
def init_engine():
    ##### get parameter
    try:
        parameters = request.get_json(force=True)
        app.logger.info(f"TEST: {parameters}")
        names = parameters.get("names")
        avatars = parameters.get("avatars")
        is_reset_words = parameters.get("words", False)
    except:
        names = request.args.get("names").replace(" ", "")
        names = names.split(",")
        avatars = request.args.get("avatars")
        if avatars is not None:
            avatars = avatars.replace(" ", "")
            avatars = avatars.split(",")
        is_reset_words = request.args.get("words", False)
    app.logger.info(f"start /init_engine {names=} {avatars=} {is_reset_words=}")

    # set reset words
    if isinstance(is_reset_words, str):
        is_reset_words = is_reset_words.lower() == "true"

    if is_reset_words is True:
        ENGINE.reset()
        app.logger.info(f"start /init_engine reset_word")

    try:
        ENGINE.init_engine(names=names, avatar_list=avatars)
        app.logger.info(ENGINE)
        return "ok"

    except Exception as e:
        app.logger.info(e)
        return Response(e.args[0], status=500, mimetype="application/json")


@app.route("/reset_word", methods=["GET"])  # reset word inside randomizer
def reset():
    app.logger.info(f"start /reset_word")
    ENGINE.reset()
    app.logger.info(ENGINE)
    return "OK"


@app.route("/check_status", methods=["GET"])
def check_status():
    app.logger.info(f"start /check_status")
    return jsonify({"num_word": len(ENGINE.randomizer)})


@app.route("/add", methods=["POST"])  # add word to the randomizer
def add():
    try:
        word = request.get_json(force=True)["word"]
    except:
        word = request.args.get("word")
    app.logger.info(f"start /add {word=}")
    try:
        msg = ENGINE.add(word)
        app.logger.info(ENGINE)
        app.logger.info(msg)
        return jsonify({"message": msg})

    except AssertionError as e:  # duplicated word
        app.logger.info(e)
        return (
            jsonify({"message": e.args[0]}),
            500,
        ) 

@app.route("/random", methods=["GET"])
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
        return jsonify({"message": e.args[0]}), 500


if __name__ == "__main__":
    app.run(debug=True)
