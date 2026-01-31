import pytest
from src.core.domain.unit_converter import km_to_mph, mph_to_km


class TestUnitConverter:
    def test_km_to_mph_zero(self):
        assert km_to_mph(0) == 0

    def test_km_to_mph_positive(self):
        result = km_to_mph(100)
        assert abs(result - 62.1371) < 0.001

    def test_km_to_mph_decimal(self):
        result = km_to_mph(50.5)
        assert abs(result - 31.379) < 0.01

    def test_mph_to_km_zero(self):
        assert mph_to_km(0) == 0

    def test_mph_to_km_positive(self):
        result = mph_to_km(62.1371)
        assert abs(result - 100) < 0.001

    def test_mph_to_km_decimal(self):
        result = mph_to_km(31.379)
        assert abs(result - 50.5) < 0.1

    def test_round_trip_conversion(self):
        original_kph = 120.5
        mph = km_to_mph(original_kph)
        back_to_kph = mph_to_km(mph)
        assert abs(back_to_kph - original_kph) < 0.001
