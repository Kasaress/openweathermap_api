import pytest
from apscheduler.job import Job
from apscheduler.triggers.interval import IntervalTrigger

from apps.home.models import City, Weather
from apps.home.tasker import _weather_job, weather_job


class TestGeoManager:
    @pytest.mark.parametrize(
    'city_name, expected_lat, expected_lon',
        [
            ('barnaul', 53.347402, 83.7784496),  # Город, которого нет в БД
            ('London', 51.5073219, -0.1276474),  # Город, который есть в БД
            ('dwefwe', None, None)  # Город, которого вообще не существует
        ]
    )
    def test_get_coordinates(self, geo_manager, city_name, expected_lat, expected_lon):
        lat, lon = geo_manager.get_coordinates(city_name)
        assert lat == expected_lat
        assert lon == expected_lon
        

class TestWeatherManager:
    @pytest.mark.parametrize(
    'lat, lon',
        [
            (53.347402, 83.7784496),  # Координаты Барнаула
            (51.5073219, -0.1276474),  # Координаты Лондона
        ]
    )
    def test_get_temperature(self, weather_manager, lat, lon):
        temp = weather_manager.get_temperature(lat, lon)
        assert temp is not None
        assert type(temp) == float
        
    @pytest.mark.parametrize(
        'lat, lon',
        [(None, None)]
    )
    def test_get_temperature_fail(self, weather_manager, lat, lon):
        temp = weather_manager.get_temperature(lat, lon)
        assert temp is None


class TestCollector:
    def test_update_temp(self, collector, db):
        city = db.session.query(City).filter_by(name='barnaul').first()
        assert city is not None
        assert city.name == 'barnaul'
        collector.update_temp('barnaul')
        weather = db.session.query(Weather).filter_by(city_id=city.id).first()
        assert weather is not None
        old_update = weather.edited_at
        collector.update_temp('barnaul')
        new_update = weather.edited_at
        assert old_update != new_update


class TestSchedulerJob:
    @pytest.mark.skip()  # Долго проходит, но можно закомментить
    def test_weather_job(self):
        _weather_job()  # Пока не придумала как потестить, смотрим глазами
    
    def test_scheduler_tasks(self, scheduler):
        a_scheduled_function_job: Job = scheduler.get_job(id="Обновление температуры")

        assert a_scheduled_function_job is not None
        assert a_scheduled_function_job.func == weather_job

        trigger: IntervalTrigger = a_scheduled_function_job.trigger

        assert isinstance(trigger, IntervalTrigger)
        assert trigger.end_date is None

