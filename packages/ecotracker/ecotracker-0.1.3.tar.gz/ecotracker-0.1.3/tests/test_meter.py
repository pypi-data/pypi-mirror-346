"""Unit tests for the EcoTracker class by everHome."""

import unittest
from unittest.mock import patch, Mock, AsyncMock
import json
import asyncio
import aiohttp

from ecotracker import EcoTracker


class TestEcoTracker(unittest.TestCase):
    """Test cases for the EcoTracker class by everHome."""

    def setUp(self):
        """Set up the test case."""
        self.meter = EcoTracker("192.168.1.100")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def test_init(self):
        """Test the initialization of the EcoTracker class."""
        self.assertEqual(self.meter.ip_address, "192.168.1.100")
        self.assertEqual(self.meter.port, 80)
        self.assertEqual(self.meter.endpoint, "http://192.168.1.100:80/v1/json")
        self.assertEqual(self.meter.data, {})

    @patch("ecotracker.meter.requests.get")
    def test_update_success(self, mock_get):
        """Test the update method with a successful response."""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {
            "power": 1000.5,
            "powerPhase1": 300.1,
            "powerPhase2": 350.2,
            "powerPhase3": 350.2,
            "powerAvg": 950.0,
            "energyCounterOut": 500.5,
            "energyCounterIn": 1500.5,
            "energyCounterInT1": 1000.0,
            "energyCounterInT2": 500.5
        }
        mock_get.return_value = mock_response

        # Call the update method
        result = self.meter.update()

        # Verify the result
        self.assertTrue(result)
        mock_get.assert_called_once_with(self.meter.endpoint, timeout=10)
        self.assertEqual(self.meter.get_power(), 1000.5)
        self.assertEqual(self.meter.get_power_phase1(), 300.1)
        self.assertEqual(self.meter.get_power_phase2(), 350.2)
        self.assertEqual(self.meter.get_power_phase3(), 350.2)
        self.assertEqual(self.meter.get_power_avg(), 950.0)
        self.assertEqual(self.meter.get_energy_counter_out(), 500.5)
        self.assertEqual(self.meter.get_energy_counter_in(), 1500.5)
        self.assertEqual(self.meter.get_energy_counter_in_t1(), 1000.0)
        self.assertEqual(self.meter.get_energy_counter_in_t2(), 500.5)

    @patch("ecotracker.meter.requests.get")
    def test_update_missing_fields(self, mock_get):
        """Test the update method with missing fields in the response."""
        # Mock response data with missing fields
        mock_response = Mock()
        mock_response.json.return_value = {
            "power": 1000.5,
            "powerAvg": 950.0,
            "energyCounterIn": 1500.5
        }
        mock_get.return_value = mock_response

        # Call the update method
        result = self.meter.update()

        # Verify the result
        self.assertTrue(result)
        self.assertEqual(self.meter.get_power(), 1000.5)
        self.assertIsNone(self.meter.get_power_phase1())
        self.assertIsNone(self.meter.get_power_phase2())
        self.assertIsNone(self.meter.get_power_phase3())
        self.assertEqual(self.meter.get_power_avg(), 950.0)
        self.assertIsNone(self.meter.get_energy_counter_out())
        self.assertEqual(self.meter.get_energy_counter_in(), 1500.5)
        self.assertIsNone(self.meter.get_energy_counter_in_t1())
        self.assertIsNone(self.meter.get_energy_counter_in_t2())

    @patch("ecotracker.meter.requests.get")
    def test_update_request_exception(self, mock_get):
        """Test the update method with a request exception."""
        # Mock a request exception
        mock_get.side_effect = Exception("Connection error")

        # Call the update method
        result = self.meter.update()

        # Verify the result
        self.assertFalse(result)
        self.assertEqual(self.meter.data, {})


class TestEcoTrackerAsync(unittest.TestCase):
    """Test cases for the async methods of EcoTracker class."""

    def setUp(self):
        """Set up the test case."""
        self.meter = EcoTracker("192.168.1.100")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.mock_session = Mock(spec=aiohttp.ClientSession)

    def tearDown(self):
        """Clean up after the test case."""
        self.loop.close()

    def test_async_update_success(self):
        """Test the async_update method with a successful response."""
        # Mock response data
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.closed = False
        mock_response.close = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "power": 1000.5,
            "powerPhase1": 300.1,
            "powerPhase2": 350.2,
            "powerPhase3": 350.2,
            "powerAvg": 950.0,
            "energyCounterOut": 500.5,
            "energyCounterIn": 1500.5,
            "energyCounterInT1": 1000.0,
            "energyCounterInT2": 500.5
        })
        mock_response.raise_for_status = AsyncMock()
        
        # Mock the session's get method
        self.mock_session.get = AsyncMock(return_value=mock_response)

        # Call the async_update method
        result = self.loop.run_until_complete(self.meter.async_update(self.mock_session))

        # Verify the result
        self.assertTrue(result)
        self.assertEqual(self.meter.get_power(), 1000.5)
        self.assertEqual(self.meter.get_power_phase1(), 300.1)
        self.assertEqual(self.meter.get_power_phase2(), 350.2)
        self.assertEqual(self.meter.get_power_phase3(), 350.2)
        self.assertEqual(self.meter.get_power_avg(), 950.0)
        self.assertEqual(self.meter.get_energy_counter_out(), 500.5)
        self.assertEqual(self.meter.get_energy_counter_in(), 1500.5)
        self.assertEqual(self.meter.get_energy_counter_in_t1(), 1000.0)
        self.assertEqual(self.meter.get_energy_counter_in_t2(), 500.5)

    def test_async_update_http_error(self):
        """Test the async_update method with an HTTP error."""
        # Mock response with error
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.closed = False
        mock_response.close = AsyncMock()
        mock_response.raise_for_status = AsyncMock(side_effect=aiohttp.ClientResponseError(
            request_info=Mock(),
            history=(),
            status=404,
            message="Not Found"
        ))
        
        # Mock the session's get method
        self.mock_session.get = AsyncMock(return_value=mock_response)

        # Call the async_update method
        result = self.loop.run_until_complete(self.meter.async_update(self.mock_session))

        # Verify the result
        self.assertFalse(result)
        self.assertEqual(self.meter.data, {})

    def test_async_update_exception(self):
        """Test the async_update method with a general exception."""
        # Mock a connection error
        self.mock_session.get = AsyncMock(side_effect=aiohttp.ClientError("Connection error"))

        # Call the async_update method
        result = self.loop.run_until_complete(self.meter.async_update(self.mock_session))

        # Verify the result
        self.assertFalse(result)
        self.assertEqual(self.meter.data, {})


if __name__ == "__main__":
    unittest.main()