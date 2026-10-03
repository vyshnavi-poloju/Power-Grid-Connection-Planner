from flask import Flask, render_template, jsonify

from graph import graph
from main_code import kruskal


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run")
def run():
    mst,cost = kruskal(graph)

    return jsonify({"result": f"MST Cost={cost},Edges={mst}"})

if __name__ == "__main__":
    app.run(debug=True)