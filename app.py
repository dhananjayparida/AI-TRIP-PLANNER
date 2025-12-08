from flask import Flask, render_template, jsonify, request
import aitrip as at
from flask_cors import CORS as cs

app = Flask(__name__)
cs(app)

@app.route('/')
def home():
    return "Welcome to the Smart Trip Planner API!"

@app.route('/Smart_Trip_Planner/<string:source>/<string:destination>/<int:days>/<int:budget>', methods=['GET', 'OPTIONS'])
def smart_trip_planner(source, destination, days, budget):
    if request.method == 'OPTIONS':
        return '', 200
    trip_data = at.generate_trip_plan(source, destination, days, budget)
    return jsonify(trip_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
