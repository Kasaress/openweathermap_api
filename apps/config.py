# -*- encoding: utf-8 -*-
from threading import Lock
import os
import yaml
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class ConfigClass(object):
    """Класс ConfigClass служит для чтения config.yaml файла.
    """
    def __init__(self, filename):
        self._lock = Lock()
        self.filename = filename
        self.load = "abc"
        with open(self.filename, "r") as stream:
            try:
                self.load = yaml.safe_load(stream)
                for i in self.load:
                    setattr(self, i, self.load[i])
            except yaml.YAMLError as exc:
                print("Ошибка чтения конфиг файла", exc)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, item):
        with self._lock:
            namespace = item.split(".")
            data = self.load
            for name in namespace:
                data = data[name]
            return data


class Config(ConfigClass):
    """Класс Config служит для установки
    переменных окружения данного модуля.
    """
    def __init__(self, filename):
        ConfigClass.__init__(self, filename)
        db_path = os.path.join(os.path.dirname(__file__), 'app.db')
        db_uri = 'sqlite:///{}'.format(db_path)
        self.SQLALCHEMY_DATABASE_URI = db_uri
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
        self.SCHEDULER_JOBSTORES = {
            "default": SQLAlchemyJobStore(
                url=self.SQLALCHEMY_DATABASE_URI, tablename="TaskCalendarDMZ"
            )
        }
        self.SCHEDULER_API_ENABLED = True
        self.SCHEDULER_TIMEZONE = "Europe/Moscow"


# Загрузка всех конфигураций
config = Config("./config.yaml")
