from flask import Flask, render_template, request, jsonify
import aitrip as at

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home(): 
    return "hello"

@app.route('/Smart_Trip_Planner/<string:source>/<string:destination>/<int:days>/<int:budget>', methods=['GET'])
def smart_trip_planner(source , destination, days, budget):
    detail=at.generate_trip_plan(source, destination, days, budget).replace("\n", "<br>")
    return jsonify(detail)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
