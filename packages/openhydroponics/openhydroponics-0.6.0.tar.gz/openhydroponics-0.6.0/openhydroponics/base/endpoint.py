from enum import IntEnum
import logging
from typing import Any

from openhydroponics.signal import signal

_LOG = logging.getLogger(__name__)


class EndpointClass(IntEnum):
    """
    Endpoint class types.
    These classes are used to categorize the type of endpoint in a node.
    """
    NotSupported = 0
    """Not supported"""
    Input = 1
    """Input endpoint"""
    Output = 2
    """Output endpoint"""


class EndpointInputClass(IntEnum):
    """
    Endpoint input class types.
    These classes are used to categorize the type of input endpoint in a node.
    """
    NotSupported = 0
    """Not supported"""
    Temperature = 1
    """Temperature endpoint"""
    Humidity = 2
    """Humidity endpoint"""
    EC = 3
    """Electrical Conductivity endpoint"""
    PH = 4
    """pH endpoint"""


class EndpointOutputClass(IntEnum):
    """
    Endpoint output class types.
    These classes are used to categorize the type of output endpoint in a node.
    """
    NotSupported = 0
    """Not supported"""
    Variable = 1
    """Variable output endpoint"""
    Binary = 2
    """Binary output endpoint"""


class Endpoint:
    """
    Base class for all endpoints.
    This class provides a common interface for all endpoint types.
    """
    ENDPOINT_CLASS = EndpointClass.NotSupported

    def __init__(self, node, endpoint_id: int):
        self._node = node
        self._endpoint_id: int = endpoint_id

    @property
    def endpoint_id(self) -> int:
        """
        Get the endpoint number for this endpoint.

        :returns: The endpoint's identifier that distinguishes it from other endpoints in this node.
        """
        return self._endpoint_id

    async def init(self):
        """
        Initialize the endpoint.

        This method is called to set up the endpoint after it has been created.
        It can be used to perform any necessary setup or configuration.
        """
        pass

    async def interview(self):
        """
        Conducts an interactive interview process for endpoint configuration.

        This asynchronous method prompts for and collects necessary information
        to set up or configure the endpoint.
        """
        pass

    @property
    def node(self):
        """
        Returns the node associated with this endpoint.
        """
        return self._node

    async def get_config(self, config: int) -> dict[str, Any]:
        """
        Get configuration parameters for this endpoint.

        This method retrieves the current configuration settings for the endpoint.

        :param config: The configuration number to retrieve.
        :returns: The value of the requested configuration parameter.
        """
        pass

    async def set_config(self, config: dict[str, Any]) -> bool:
        """
        Set configuration parameters for this endpoint.

        This method updates the endpoint's configuration with the provided dictionary of settings.

        :param config: A dictionary containing configuration parameters where keys are parameter names and values are the
            parameter values. This can include settings like thresholds, calibration values, or other endpoint-specific
            configurations.
        :returns: True if the configuration was successfully set, False otherwise.
        """
        pass


class InputEndpoint(Endpoint):
    ENDPOINT_CLASS = EndpointClass.Input
    INPUT_CLASS = EndpointInputClass.NotSupported

    def __init__(self, node, endpoint_id):
        super().__init__(node, endpoint_id)
        self._value = None
        self._scale = None

    @signal()
    def on_value_changed(self, value: float, scale: int):
        """
        Signal emitted when a sensor reading is received.

        :param value: The value of the sensor reading.
        :param scale: The scale of the sensor reading.
        """

    @property
    def value(self):
        return self._value

    @property
    def scale(self):
        return self._scale

    def update(self, value: float, scale: int):
        """
        Update the endpoint with a new sensor reading.

        :param value: The value of the sensor reading.
        :param scale: The scale of the sensor reading.
        """
        self._value = value
        self._scale = scale
        self.on_value_changed(value, scale)


class TemperatureEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Temperature


class HumidityEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Humidity


class OutputEndpoint(Endpoint):
    ENDPOINT_CLASS = EndpointClass.Output
    OUTPUT_CLASS = EndpointOutputClass.NotSupported


class VariableOutputEndpoint(OutputEndpoint):
    OUTPUT_CLASS = EndpointOutputClass.Variable

    def __init__(self, node, endpoint_id):
        super().__init__(node, endpoint_id)
        self._value = 0

    async def set(self, value: float):
        """
        Set the output value for this endpoint.

        :param value: The value to set for the output.
        """
        pass

    def update(self, value: float):
        """
        Update the endpoint with a new output value.

        :param value: The value of the output.
        """
        self._value = value
        self.on_value_changed(value)

    @property
    def value(self):
        """
        Get the current output value for this endpoint.

        :returns: The current output value.
        """
        return self._value

    @signal()
    def on_value_changed(self, value: float):
        """
        Signal emitted when a new output value is set.
        :param value: The new output value.
        """


class ECConfigWriteType(IntEnum):
    LOW = 0
    HIGH = 1
    GAIN = 2
    RAW = 3


class ECConfigReadType(IntEnum):
    CALIBRATION = 0
    RAW = 1


class ECEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.EC


class PHConfigWriteType(IntEnum):
    LOW = 0
    MID = 1  # Not all frontends support this
    HIGH = 2
    RAW = 3


class PHConfigReadType(IntEnum):
    RAW = 0
    CALIBRATION = 1
    SLOPE = 2


class PHEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.PH
