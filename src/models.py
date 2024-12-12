from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    clima = db.Column(db.String, nullable=True)
    terreno = db.Column(db.String, nullable=True)
    poblacion = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    genero = db.Column(db.String, nullable=True)
    altura = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Integer, nullable=True)
    especie = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "altura": self.altura,
            "peso": self.peso,
            "especie": self.especie,
        }

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    modelo = db.Column(db.String, nullable=True)
    costo = db.Column(db.Integer, nullable=True)
    combustible = db.Column(db.Integer, nullable=True)
    asientos = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Vehiculo %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "costo": self.costo,
            "combustible": self.combustible,
            "asientos": self.asientos,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=True)

    user = db.relationship('User', backref='favorites', lazy=True)
    planet = db.relationship('Planet', backref='favorites', lazy=True)
    people = db.relationship('People', backref='favorites', lazy=True)
    vehiculo = db.relationship('Vehiculo', backref='favorites', lazy=True)

    def __repr__(self):
        return f'<favorite {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "vehiculo_id": self.vehiculo_id,
        }
