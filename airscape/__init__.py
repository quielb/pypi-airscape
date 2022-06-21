"""Module for Controlling AirScape Whole House Fans."""
__version__ = "0.1.9.4.1"

import re
import json
from time import sleep
import requests

from . import exceptions as ex
from .const import MAX_FAN_SPEED, DEFAULT_TIMEOUT, STATUS_KEYS, CAST_TO_INT


class Fan:
    """Class representing an Airscape whole house fan.

    Constructor has one required parameter.
    IP or host name of fan to control.
    """

    def __init__(self, host, timeout=DEFAULT_TIMEOUT):
        """Initialize a fan."""
        self._command_api = "http://" + host + "/fanspd.cgi"
        self._status_api = "http://" + host + "/fanspd.cgi?dir"
        self._timeout = timeout
        self._data = {}
        self.get_device_state()

    @property
    def is_on(self) -> bool:
        """Get the fan state.

        True if on. False if off.
        """
        return bool(self._data["fanspd"])

    @is_on.setter
    def is_on(self, state: bool) -> None:
        """Set the fan state.

        True on. False off.
        """
        if state and not bool(self._data["fanspd"]):
            self.set_device_state(1)
            # Need to pause here and wait for damper doors to open.
            # Fan doesn't start or report fanspd > 0
            # until doors have opened far enough.
            while bool(self._data["doorinprocess"]):
                sleep(0.25)
                self.get_device_state()
        elif not state:
            self.set_device_state(4)

    @property
    def speed(self) -> int:
        """Get the fan speed.

        Returns int between 0 and MAX_FAN_SPEED.
        """
        return self._data["fanspd"]

    @speed.setter
    def speed(self, speed: int) -> None:
        """Set the fan speed to a specific rate.

        Fan is not required to be on to set the speed.
        It will turn on and then adjust to specified speed.
        """
        # Speed of 0 is assumed to mean off
        if speed == 0:
            self.is_on = False
            return

        # Turn on and wait for damper doors before speeding up
        if not self.is_on:
            self.is_on = True

        command = 1
        if speed < self._data["fanspd"]:
            command = 3

        last_speed = self._data["fanspd"]
        while speed != self._data["fanspd"]:
            self.set_device_state(command)
            sleep(0.75)
            if last_speed == self._data["fanspd"]:
                break
            last_speed = self._data["fanspd"]

    @property
    def max_speed(self):
        """Return maximum speed of fan."""
        return MAX_FAN_SPEED.get(self._data["model"], MAX_FAN_SPEED["default"])

    def speed_up(self):
        """Increase fan speed by 1."""
        if (
            1
            <= self._data["fanspd"]
            < MAX_FAN_SPEED.get(self._data["model"], MAX_FAN_SPEED["default"])
        ):
            self.set_device_state(1)

    def slow_down(self):
        """Decrease fan speed by 1."""
        if self._data["fanspd"] > 1:
            self.set_device_state(3)

    def add_time(self):
        """Add 1 hour to the shutoff timer."""
        self.set_device_state(2)

    def get_device_state(self, fan_state=None):
        """Get refresh data from fan.

        Function returns Dict of fan state data.
        """

        if fan_state is None:
            try:
                api = requests.get(self._status_api, timeout=self._timeout)
                fan_state = api.text
            except requests.exceptions.ConnectionError:
                raise ex.ConnectionError from requests.exceptions.ConnectionError
            except requests.exceptions.ReadTimeout:
                raise ex.Timeout from requests.exceptions.ReadTimeout
        # Parse through the string return data for STATUS_KEYS{}
        for k, v in STATUS_KEYS.items():
            re_pattern = "(<" + v + ">)(.*)(<\/" + v + ">)"
            self._data[k] = re.search(re_pattern, fan_state).group(2)
            if k in CAST_TO_INT:
                self._data[k] = int(self._data[k])
        return self._data

    def set_device_state(self, cmd) -> None:
        """Set state of fan.

        Calls the fan API via GET.  Only has one supported parameter: dir
        Possible int values for dir:
        1: speed up (also causes fan to turn on)
        2: Add an hour to the shutoff timer
        3: slow down one speed increment
        4: Turn off (slowing down to speed of 0 does not turn off fan)
        """
        try:
            api = requests.get(
                self._command_api, params={"dir": cmd}, timeout=self._timeout
            )
            self.get_device_state(api.text)
        except requests.exceptions.ConnectionError:
            raise ex.ConnectionError from requests.exceptions.ConnectionError
        except requests.exceptions.ReadTimeout:
            raise ex.Timeout from requests.exceptions.ReadTimeout
