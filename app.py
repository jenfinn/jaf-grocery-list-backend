from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Food(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done

class FoodSchema(ma.Schema):
    class Meta:
        fields = ("id", "title","done")
        
food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)

# alwayw two arguments
@app.route("/items", methods=["GET"])
def get_foods():
    all_foods = Food.query.all()
    result = foods_schema.dump(all_foods)
    return jsonify(result)

@app.route("/food", methods=["POST"])
def add_food():
    title = request.args["title"]
    done = request.args["done"].lower() == "true"

    new_food = Food(title, done)
    db.session.add(new_food)
    db.session.commit()
    
    created_food = Food.query.get(new_food.id)
    return food_schema.jsonify(created_food)

@app.route("/food/<id>", methods=["PUT"])
def update_food(id):
    food = Food.query.get(id)

    food.title = request.args["title"]
    food.done = request.args["done"].lower() == "true"

    db.session.commit()
    return food_schema.jsonify(food)

@app.route("/food/<id>", methods=["DELETE"])
def delete_food(id):
    food = Food.query.get(id)

    db.session.delete(food)
    db.session.commit()

    return "RECORD DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()

    response