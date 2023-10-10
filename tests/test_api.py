import pytest


class TestGeomanager:
    @pytest.mark.parametrize(
    'city_name',
    [
        'barnaul',
        'London',
        'dwefwe'
    ]
    )
    def test_geo_manager(self, geo_manager, city_name):
        lat, lon = geo_manager.get_coordinates(city_name)
        assert lat is not None
        assert lon is not None