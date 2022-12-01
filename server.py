from flask import Flask, render_template, request
import dialogues
import json

# from werkzeug.middleware.profiler import ProfilerMiddleware
script = json.load(open("./pre_generated/ad-lib.json"))
paraphrases = json.load(open("./pre_generated/paraphrases.json"))
DIALOGUE = dialogues.Dialogue(
    "./pre_generated/ad-lib.json", "./pre_generated/paraphrases.json"
)

app = Flask(
    __name__, template_folder="./flask/templates/", static_folder="./flask/static/"
)

@app.route("/")
def home():
    """Home Page"""
    return render_template("index.html")


@app.route("/speech", methods=["POST"])
def speech():
    json = request.get_json()
    dialogue = dialogues.Dialogue(script, paraphrases)
    dialogue.set_state(json["state"])
    text = dialogue.progress(json["resp"])
    resp = {"speech": text, "state": dialogue.get_state()}
    return resp, 200
