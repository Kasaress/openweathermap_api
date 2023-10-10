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

# import datetime
# # from apps import db
# from typing import List
# from typing import Optional
# from sqlalchemy import ForeignKey
# from sqlalchemy import String, Integer, DateTime, Float
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship


# class Base(DeclarativeBase):
#     pass


# class City(Base):
#     __tablename__ = 'City'

#     id = mapped_column(
#         Integer,
#         primary_key=True,
#         unique=True,
#         autoincrement=True
#     )
#     uuid = mapped_column(String(20), unique=True)
#     name = mapped_column(String(30), unique=True)
#     created_at = mapped_column(DateTime, default=datetime.datetime.utcnow)
#     edited_at = mapped_column(
#         DateTime,
#         default=datetime.datetime.utcnow,
#         onupdate=datetime.datetime.utcnow
#     )
#     latitude = mapped_column(Float)
#     longitude = mapped_column(Float)
#     weather_id = mapped_column(Integer, ForeignKey("Weather.id"))

#     def __repr__(self):
#         return self.name

#     def created_at_formatted(self):
#         return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

#     def edited_at_formatted(self):
#         return self.edited_at.strftime("%d-%m-%Y %H:%M:%S")


# class Weather(Base):
#     __tablename__ = 'Weather'

#     id = mapped_column(
#         Integer,
#         primary_key=True,
#         unique=True,
#         autoincrement=True
#     )
#     city_id = mapped_column(Integer, ForeignKey("City.id"))
#     created_at = mapped_column(DateTime, default=datetime.datetime.utcnow)
#     edited_at = mapped_column(
#         DateTime,
#         default=datetime.datetime.utcnow,
#         onupdate=datetime.datetime.utcnow
#     )
#     temperature = mapped_column(Integer)

#     def __repr__(self):
#         return str(self.temperature)

#     def created_at_formatted(self):
#         return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

#     def edited_at_formatted(self):
#         return self.edited_at.strftime("%d-%m-%Y %H:%M:%S")
