from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
import aitrip as at

app = Flask(__name__)

api = Api(app)

@app.route('/', methods=['GET'])
def home(): 
    return "hello"

@app.route('/Smart_Trip_Planner/<string:source>/<string:destination>/<int:days>/<int:budget>', methods=['GET'])
def smart_trip_planner(source , destination, days, budget):
    detail=at.generate_trip_plan(source, destination, days, budget).replace("\n", "<br>")
    return jsonify(detail)


app.run(debug=True)
