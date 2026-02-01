import pytest
from src.core.domain.rpm_calculator import RPMCalculator


class TestRPMCalculator:
    def setup_method(self):
        self.gear_ratios = {
            -1: -3.5,
            0: 0.0,
            1: 3.08,
            2: 2.19,
            3: 1.71,
            4: 1.39,
            5: 1.16,
            6: 1.00,
        }
        self.calculator = RPMCalculator(
            gear_ratios=self.gear_ratios,
            final_drive=3.5,
            wheel_circumference=1.9,
            idle_rpm=1500,
            max_rpm=8000,
        )

    def test_neutral_gear_returns_idle_rpm(self):
        rpm = self.calculator.calculate(speed_kmh=100.0, gear=0)
        assert rpm == 1500

    def test_reverse_gear_calculation(self):
        rpm = self.calculator.calculate(speed_kmh=20.0, gear=-1)
        assert rpm >= 1500
        assert rpm <= 8000

    def test_low_speed_returns_idle_rpm(self):
        rpm = self.calculator.calculate(speed_kmh=0.1, gear=3)
        assert rpm == 1500

    def test_normal_speed_calculation(self):
        rpm = self.calculator.calculate(speed_kmh=100.0, gear=3)
        assert rpm > 1500
        assert rpm < 8000

    def test_high_speed_clamped_to_max_rpm(self):
        rpm = self.calculator.calculate(speed_kmh=500.0, gear=1)
        assert rpm == 8000

    def test_different_gears_different_rpm(self):
        rpm_gear_2 = self.calculator.calculate(speed_kmh=100.0, gear=2)
        rpm_gear_4 = self.calculator.calculate(speed_kmh=100.0, gear=4)

        assert rpm_gear_2 > rpm_gear_4

    def test_higher_speed_higher_rpm(self):
        rpm_50 = self.calculator.calculate(speed_kmh=50.0, gear=3)
        rpm_150 = self.calculator.calculate(speed_kmh=150.0, gear=3)

        assert rpm_150 > rpm_50

    def test_invalid_gear_uses_default_ratio(self):
        rpm = self.calculator.calculate(speed_kmh=100.0, gear=99)
        assert rpm >= 1500
        assert rpm <= 8000
