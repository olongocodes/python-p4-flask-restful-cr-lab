#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Initialize the database (create tables)
with app.app_context():
    db.create_all()

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_data = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plants_data), 200)

    def post(self):
        data = request.json
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()

        response_data = new_plant.to_dict()
        return make_response(jsonify(response_data), 201)

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            plant_data = plant.to_dict()
            return make_response(jsonify(plant_data), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

# Associate the resource classes with routes
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
