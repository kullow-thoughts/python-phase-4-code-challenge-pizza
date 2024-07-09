#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

#####get request retrieves restaurants. I am gonna test the RESTful and route ways
# @app.route("/restaurants", methods=['GET'])
# def get_restaurants():
#     restaurant_list = [restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in Restaurant.query.all()]
#     response = make_response(restaurant_list, 200)
#     return response
class Restaurants(Resource):
    def get(self):
        restaurant_list = [restaurant.to_dict(rules=('-restaurant_pizzas', )) for restaurant in Restaurant.query.all()]
        response = make_response(restaurant_list, 200)
        return response

#handles get request  for a single restaurant
class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            
            response = make_response(restaurant_dict, 200)
            return response
        else:
            response = make_response({"error": "Restaurant not found"}, 404)
            return response
        
    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({}, 204)
        else:
            response = make_response({"error": "Restaurant not found"}, 404)
            return response

class Pizzas(Resource):
    def get(self):
        pizza_list = [pizza.to_dict(rules=('-restaurant_pizzas', )) for pizza in Pizza.query.all()]
        response = make_response(pizza_list, 200)
        return response
    
class RestPizzas(Resource):
    def post(self):
        data = request.get_json()
        new_price = data.get('price')
        new_restaurant_id = data.get('restaurant_id')
        new_pizza_id = data.get('pizza_id')

        if new_price < 1:
            return make_response({'errors' : ["validation errors"]}, 400)
        elif new_price > 30:
            return make_response({'errors' : ["validation errors"]}, 400)
        else:
            new_validated_price = new_price

        new_restaurant_pizza = RestaurantPizza(
            price = new_validated_price,
            pizza_id = new_pizza_id,
            restaurant_id = new_restaurant_id
        )
       
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        new_restaurant_pizza_dict = new_restaurant_pizza.to_dict()
        response = make_response(new_restaurant_pizza_dict, 201)
        return response
        
        




api.add_resource(Restaurants, '/restaurants', endpoint='restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>', endpoint='restaurantbyid')
api.add_resource(Pizzas, '/pizzas', endpoint='pizzas')
api.add_resource(RestPizzas, '/restaurant_pizzas', endpoint='restpizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)