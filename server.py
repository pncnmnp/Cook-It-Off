from flask import Flask, render_template, request
import dialogues

# from werkzeug.middleware.profiler import ProfilerMiddleware
DIALOGUE = dialogues.Dialogue(
    "./pre_generated/ad-lib.json", "./pre_generated/paraphrases.json"
)

app = Flask(
    __name__, template_folder="./flask/templates/", static_folder="./flask/static/"
)
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5])


@app.route("/")
def home():
    """Home Page"""
    return render_template("index.html")


@app.route("/speech", methods=["POST"])
def speech():
    query = request.get_json()["resp"]
    text = DIALOGUE.progress(query)
    resp = {"speech": text}
    return resp, 200
