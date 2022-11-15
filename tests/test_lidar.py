from unittest import TestCase
from unittest.mock import patch, Mock
from SpeedDetector import lidar

class TestSpeedDetector(TestCase):
    def test_calc_distance_multiple(self):
        # Arrange
        mock_serial = Mock()
        distances = [1,2,3,4,5]
        expected_distance = 4.0

        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        actual_distance = sensor.calc_distance(distances)

        # Assert
        assert actual_distance == expected_distance

    @patch('serial.Serial')
    def test_calc_distance_single(self, mock_serial):
        # Arrange
        mock_serial.Serial = Mock()
        distances = [5]
        expected_distance = 0
        
        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        sensor.setup_serial()
        actual_distance = sensor.calc_distance(distances)

        # Assert
        assert actual_distance == expected_distance
        
    @patch('serial.Serial')
    def test_calc_speed_250ms_interval(self, mock_serial):
        # Arrange
        mock_serial.Serial = Mock()
        mock_serial.Serial.in_waiting.return_value = 9
        mock_serial.Write = {}
        mock_serial.Read = {}
        distance = 5
        interval = 250
        expected_speed = 20 # distance / (interval / 1000) #20

        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        sensor.setup_serial()
        actual_speed = sensor.calc_speed(distance, interval)

        # Assert
        assert actual_speed == expected_speed
        
    def test_calc_speed_1000ms_interval(self):
        # Arrange
        mock_serial = Mock()
        distance = 5
        interval = 1000
        expected_speed = 5 #distance / (interval / 1000)

        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        sensor.setup_serial()
        actual_speed = sensor.calc_speed(distance, interval)

        # Assert
        assert actual_speed == expected_speed

    def test_calc_speed_2000ms_interval(self):
        # Arrange
        mock_serial = Mock()
        distance = 5
        interval = 2000
        expected_speed = 2.5 # distance / (interval / 1000)

        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        sensor.setup_serial()
        actual_speed = sensor.calc_speed(distance, interval)

        # Assert
        assert actual_speed == expected_speed

    def test_convert_cms_mph(self):
        # Arrange
        mock_serial = Mock()
        cms_speed = 35
        mph_speed = cms_speed / 44.704

        # Act
        sensor = lidar.SpeedDetector(mock_serial)
        actual_speed = sensor.convert_cms_mph(cms_speed)

        # Assert
        assert actual_speed == mph_speed
 