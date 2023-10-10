import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from apps.home.models import City
from modules.collector import Collector


@pytest.fixture(scope="session")
def app():
    from apps import create_app
    from apps.config import config
    app = create_app(config)
    app.testing = True
    return app


@pytest.fixture(scope="session")
def geo_manager():
    from apps import geo_manager
    return geo_manager


@pytest.fixture(scope="session")
def weather_manager():
    from apps import weather_manager
    return weather_manager


@pytest.fixture(scope="session")
def scheduler():
    from apps import scheduler
    return scheduler


@pytest.fixture(scope="session")
def collector(geo_manager, weather_manager):
    return Collector(geo_manager, weather_manager)


@pytest.fixture(scope="session")
def db():
    try:
        from apps import db
        db.session.expire_on_commit = False
        return db
    except Exception:
        return None


@pytest.yield_fixture(scope="session", autouse=True)
def tear_up_down_db(db: SQLAlchemy, app: Flask):
    with app.app_context():
        try:
            obj_city = City(
                name='barnaul',
                latitude=10,
                longitude=10
            )
            db.session.add(obj_city)
            db.session.commit()

        except Exception as e:
            db.session.rollback()

        yield

        db.session.query(City).filter(City.name == 'barnaul').delete()
        db.session.commit()

