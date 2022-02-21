from flask import Flask
from markupsafe import escape


app = Flask(__name__)

@app.route("/<neighborhood>")
def is_neighborhood(neighborhood):
    return f"You asked about {escape(neighborhood)}"

