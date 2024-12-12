"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os,json
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_swagger import swagger # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planet,People,Vehiculo,Favorite  # type: ignore
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if len(users) <1:
            return jsonify({"msg": "No users found"}), 404
        s_users = list(map(lambda x: x.serialize(), users))
        return jsonify(s_users), 200
    except Exception as e:
        return str(e), 500

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"msg": f"User {id} not found"}), 404
        return jsonify(user.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/user', methods=['POST'])
def add_user():
    try:
        body = json.loads(request.data)
        user = User(
            email=body["email"],
            password=body["password"],
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "User added"}), 201
        # return jsonify(user.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        body = json.loads(request.data)
        user = User.query.get(id)
        if user is None:
            return jsonify({"msg": f"User {id} not found"}), 404
        user =  User(
            email=body["email"],
            password=body["password"],
            is_active=True,
            id = id
        )
        db.session.commit()
        return jsonify(user.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"msg": f"User {id} not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": f"User {id} deleted"}), 200
    except Exception as e:
        return str(e), 500

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    try:
        fav = Favorite.query.all()
        if len(fav) <1:
            return jsonify({"msg": "No favorites found"}), 404
        s_fav = list(map(lambda x: x.serialize(), fav))
        return jsonify(s_fav), 200
    except Exception as e:
        return str(e), 500

@app.route('/users/<int:id>/favorite', methods=['GET'])
def get_one_favorite(id):
     try:
         favorite = Favorite.query.filter_by(id = id).all()
         if favorite is None:
             return jsonify({"msg": f"favorite {id} not found"}), 404
         serialized_favorites=list(map(lambda x: x.serialize(),favorite))
         return serialized_favorites, 200
     except Exception as e:
         return str(e), 500



@app.route('/planet', methods=['GET'])
def get_planets():
    try:
        planet = Planet.query.all()
        if len(planet) <1:
            return jsonify({"msg": "No planets found"}), 404
        s_planet = list(map(lambda x: x.serialize(), planet))
        return jsonify(s_planet), 200
    except Exception as e:
        return str(e), 500

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    try:
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({"msg": f"Planet {id} not found"}), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return str(e), 500
@app.route('/planet', methods=['POST'])
def add_planet():
    try:
        body = json.loads(request.data)
        planet = Planet(
            name=body["name"],
            climate=body["climate"],
            population=body["population"]
        )
        db.session.add(planet)
        db.session.commit()
        return jsonify({"msg": "Planet added"}), 201
        # return jsonify(planet.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    try:
        body = json.loads(request.data)
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({"msg": f"Planet {id} not found"}), 404
        planet =  Planet(
            name=body["name"],
            climate=body["climate"],
            population=body["population"],
            id = id
        )
        db.session.commit()
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    try:
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({"msg": f"Planet {id} not found"}), 404
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": f"Planet {id} deleted"}), 200
    except Exception as e:
        return str(e), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        body = json.loads(request.data)
        fav = Favorite(
            user_id=body["user_id"],
            planet_id=planet_id
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({"msg": "Favorite planet added"}), 201
        # return jsonify(fav.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        fav = Favorite.query.filter_by(planet_id=planet_id).first()
        if fav is None:
            return jsonify({"msg": f"Favorite planet {planet_id} not found"}), 404
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": f"Favorite planet {planet_id} deleted"}), 200
    except Exception as e:
        return str(e), 500
    

@app.route('/people', methods=['GET'])
def get_people():
    try:
        people = People.query.all()
        if len(people) <1:
            return jsonify({"msg": "No people found"}), 404
        s_people = list(map(lambda x: x.serialize(), people))
        return jsonify(s_people), 200
    except Exception as e:
        return str(e), 500

@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    try:
        people = People.query.get(id)
        if people is None:
            return jsonify({"msg": f"People {id} not found"}), 404
        return jsonify(people.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/people', methods=['POST'])
def add_people():
    try:
        body = json.loads(request.data)
        people = People(
            nombre=body["nombre"],
            genero=body["genero"],
            altura=body["altura"],
            peso=body["peso"],
            especie=body["especie"]
        )
        db.session.add(people)
        db.session.commit()
        return jsonify({"msg": "People added"}), 201
        # return jsonify(people.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/people/<int:id>', methods=['PUT'])
def update_people(id):
    try:
        body = json.loads(request.data)
        people = People.query.get(id)
        if people is None:
            return jsonify({"msg": f"People {id} not found"}), 404
        people =  People(
            nombre=body["nombre"],
            genero=body["genero"],
            altura=body["altura"],
            peso=body["peso"],
            especie=body["especie"],
            id = id
        )
        db.session.commit()
        return jsonify(people.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
    try:
        people = People.query.get(id)
        if people is None:
            return jsonify({"msg": f"People {id} not found"}), 404
        db.session.delete(people)
        db.session.commit()
        return jsonify({"msg": f"People {id} deleted"}), 200
    except Exception as e:
        return str(e), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        body = json.loads(request.data)
        fav = Favorite(
            user_id=body["user_id"],
            people_id=people_id
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({"msg": "Favorite people added"}), 201
        # return jsonify(fav.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        fav = Favorite.query.filter_by(people_id=people_id).first()
        if fav is None:
            return jsonify({"msg": f"Favorite people {people_id} not found"}), 404
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": f"Favorite people {people_id} deleted"}), 200
    except Exception as e:
        return str(e), 500
    

@app.route('/vehiculo', methods=['GET'])
def get_vehiculo():
    try:
        vehiculo = Vehiculo.query.all()
        if len(vehiculo) <1:
            return jsonify({"msg": "No vehiculo found"}), 404
        s_vehiculo = list(map(lambda x: x.serialize(), vehiculo))
        return jsonify(s_vehiculo), 200
    except Exception as e:
        return str(e), 500

@app.route('/vehiculo/<int:id>', methods=['GET'])
def get_vehiculo_id(id):
    try:
        vehiculo = Vehiculo.query.get(id)
        if vehiculo is None:
            return jsonify({"msg": f"Vehiculo {id} not found"}), 404
        return jsonify(vehiculo.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/vehiculo', methods=['POST'])
def add_vehiculo():
    try:
        body = json.loads(request.data)
        vehiculo = Vehiculo(
            nombre=body["nombre"],
            modelo=body["modelo"],
            costo=body["costo"],
            combustible=body["combustible"],
            asientos=body["asientos"]
        )
        db.session.add(vehiculo)
        db.session.commit()
        return jsonify({"msg": "Vehiculo added"}), 201
        # return jsonify(vehiculo.serialize()), 201
    except Exception as e:
        return str(e), 500

@app.route('/vehiculo/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    try:
        body = json.loads(request.data)
        vehiculo = Vehiculo.query.get(id)
        if vehiculo is None:
            return jsonify({"msg": f"Vehiculo {id} not found"}), 404
        vehiculo =  Vehiculo(
            nombre=body["nombre"],
            modelo=body["modelo"],
            costo=body["costo"],
            combustible=body["combustible"],
            asientos=body["asientos"],
            id = id
        )
        db.session.commit()
        return jsonify(vehiculo.serialize()), 200
    except Exception as e:
        return str(e), 500

@app.route('/vehiculo/<int:id>', methods=['DELETE'])
def delete_vehiculo(id):
    try:
        vehiculo = Vehiculo.query.get(id)
        if vehiculo is None:
            return jsonify({"msg": f"Vehiculo {id} not found"}), 404
        db.session.delete(vehiculo)
        db.session.commit()
        return jsonify({"msg": f"Vehiculo {id} deleted"}), 200
    except Exception as e:
        return str(e), 500

@app.route('/favorite/vehiculo/<int:vehiculo_id>', methods=['POST'])
def add_favorite_vehiculo(vehiculo_id):
    try:
        body = json.loads(request.data)
        fav = Favorite(
            user_id=body["user_id"],
            vehiculo_id=vehiculo_id
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({"msg": "Favorite vehiculo added"}), 201
        # return jsonify(fav.serialize()), 201
    except Exception as e:
        return str(e), 500
    
@app.route('/favorite/vehiculo/<int:vehiculo_id>', methods=['DELETE'])
def delete_favorite_vehiculo(vehiculo_id):
    try:
        fav = Favorite.query.filter_by(vehiculo_id=vehiculo_id).first()
        if fav is None:
            return jsonify({"msg": f"Favorite vehiculo {vehiculo_id} not found"}), 404
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": f"Favorite vehiculo {vehiculo_id} deleted"}), 200
    except Exception as e:
        return str(e), 500
    


@app.route('/favorite', methods=['GET'])
def get_favorite():
    try:
        favorite = Favorite.query.all()
        if len(favorite) <1:
            return jsonify({"msg": "No favorite found"}), 404
        s_favorite = list(map(lambda x: x.serialize(), favorite))
        return jsonify(s_favorite), 200
    except Exception as e:
        return str(e), 501



@app.route('/favorite/<int:id>', methods=['Delete'])
def delete_favorite(id):
    try:
        favorite = Favorite.query.get(id)
        if favorite is None:
            return jsonify({"msg": f"favorite {id} not found"}), 404
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": f"favorite {id} deleted"}), 200
    except Exception as e:
        return str(e), 500





















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
