from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, image, price):
        self.name = name
        self.image = image
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": float(self.price),  # Convert to float for JSON serialization
        }

    def __repr__(self):
        return f'<Plant {self.name}, {self.image}, {self.price}>'
