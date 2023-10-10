import datetime
from apps import db


class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    uuid = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(30), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    edited_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    weather_id = db.Column(db.Integer, db.ForeignKey("Weather.id"))

    def __repr__(self):
        return self.name

    def created_at_formatted(self):
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def edited_at_formatted(self):
        return self.edited_at.strftime("%d-%m-%Y %H:%M:%S")


class Weather(db.Model):
    __tablename__ = 'Weather'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    city_id = db.Column(db.Integer, db.ForeignKey("City.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    edited_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    temperature = db.Column(db.Integer)

    def __repr__(self):
        return str(self.temperature)

    def created_at_formatted(self):
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def edited_at_formatted(self):
        return self.edited_at.strftime("%d-%m-%Y %H:%M:%S")
