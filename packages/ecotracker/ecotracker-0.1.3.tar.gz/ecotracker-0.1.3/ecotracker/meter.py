"""Module for reading EcoTracker data from a local HTTP endpoint by everHome."""

import json
from typing import Dict, Optional, Union, Any, cast
import requests
import aiohttp
import asyncio
from logging import getLogger

_LOGGER = getLogger(__name__)


class EcoTracker:
    """Class for reading EcoTracker energy consumption data from a local HTTP endpoint by everHome."""

    def __init__(self, ip_address: str, port: int = 80, session: Optional[aiohttp.ClientSession] = None):
        """Initialize the EcoTracker device.

        Args:
            ip_address: The IP address of the EcoTracker device.
            port: The port number of the HTTP endpoint (default: 80).
            session: Optional aiohttp ClientSession to use for requests.
        """
        self.ip_address = ip_address
        self.port = port
        self.endpoint = f"http://{ip_address}:{port}/v1/json"
        self.data: Dict[str, Any] = {}
        self.session = session

    def update(self) -> bool:
        """Update the electricity meter data synchronously.
        
        This method is kept for backward compatibility.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            response = requests.get(self.endpoint, timeout=10)
            response.raise_for_status()
            self.data = response.json()
            return True
        except Exception as error:
            _LOGGER.error(f"Error updating EcoTracker data: {error}")
            return False
            
    async def async_update(self, session: Optional[aiohttp.ClientSession] = None) -> bool:
        """Update the electricity meter data asynchronously.
        
        Args:
            session: Optional aiohttp ClientSession to use for this request.
                     If not provided, will use the session from initialization or create a new one.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        use_session = session or self.session
        created_session = False
        response = None

        try:
            if use_session is None:
                use_session = aiohttp.ClientSession()
                created_session = True
                
            try:
                response = await use_session.get(self.endpoint, timeout=10)
                if response.status == 200:
                    self.data = await response.json()
                    return True
                else:
                    await response.raise_for_status()
                    return False
            except aiohttp.ClientResponseError as error:
                _LOGGER.error(f"HTTP error updating EcoTracker data asynchronously: {error}")
                return False
            finally:
                if response is not None and not response.closed:
                    await response.close()
        except Exception as error:
            _LOGGER.error(f"Error updating EcoTracker data asynchronously: {error}")
            return False
        finally:
            # Only close the session if we created it internally
            if created_session and use_session is not None:
                await use_session.close()

    def get_power(self) -> Optional[float]:
        """Get the current power consumption.

        Returns:
            Optional[float]: The current power consumption in watts, or None if not available.
        """
        return self.data.get("power")

    def get_power_phase1(self) -> Optional[float]:
        """Get the current power consumption of phase 1.

        Returns:
            Optional[float]: The current power consumption of phase 1 in watts, or None if not available.
        """
        return self.data.get("powerPhase1")

    def get_power_phase2(self) -> Optional[float]:
        """Get the current power consumption of phase 2.

        Returns:
            Optional[float]: The current power consumption of phase 2 in watts, or None if not available.
        """
        return self.data.get("powerPhase2")

    def get_power_phase3(self) -> Optional[float]:
        """Get the current power consumption of phase 3.

        Returns:
            Optional[float]: The current power consumption of phase 3 in watts, or None if not available.
        """
        return self.data.get("powerPhase3")

    def get_power_avg(self) -> Optional[float]:
        """Get the average power consumption.

        Returns:
            Optional[float]: The average power consumption in watts, or None if not available.
        """
        return self.data.get("powerAvg")

    def get_energy_counter_out(self) -> Optional[float]:
        """Get the energy counter for outgoing energy.

        Returns:
            Optional[float]: The energy counter for outgoing energy in kWh, or None if not available.
        """
        return self.data.get("energyCounterOut")

    def get_energy_counter_in(self) -> Optional[float]:
        """Get the energy counter for incoming energy.

        Returns:
            Optional[float]: The energy counter for incoming energy in kWh, or None if not available.
        """
        return self.data.get("energyCounterIn")

    def get_energy_counter_in_t1(self) -> Optional[float]:
        """Get the energy counter for incoming energy in tariff 1.

        Returns:
            Optional[float]: The energy counter for incoming energy in tariff 1 in kWh, or None if not available.
        """
        return self.data.get("energyCounterInT1")

    def get_energy_counter_in_t2(self) -> Optional[float]:
        """Get the energy counter for incoming energy in tariff 2.

        Returns:
            Optional[float]: The energy counter for incoming energy in tariff 2 in kWh, or None if not available.
        """
        return self.data.get("energyCounterInT2")

    def get_all_data(self) -> Dict[str, Any]:
        """Get all electricity meter data.

        Returns:
            Dict[str, Any]: All electricity meter data.
        """
        return self.data.copy()