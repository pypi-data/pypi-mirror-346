import logging

from serde import serde
from pypostcard.types import f32, u8
from pypostcard.serde import from_postcard

from openhydroponics.net.msg import ActuatorOutput, EndpointClass, SensorReading
from openhydroponics.base import endpoint as EndpointBase

_LOG = logging.getLogger(__name__)


class InputEndpoint:
    def handle_sensor_reading(self, msg: SensorReading):
        self.update(msg.value, msg.scale)


class GenericInputEndpoint(InputEndpoint, EndpointBase.InputEndpoint):
    pass


class TemperatureEndpoint(InputEndpoint, EndpointBase.TemperatureEndpoint):
    pass


class HumidityEndpoint(InputEndpoint, EndpointBase.HumidityEndpoint):
    pass


@serde
class ECConfigCalibration:
    value: f32


@serde
class ECConfigRaw:
    value: f32


@serde
class ECConfigCalibrationRaw:
    reference_low: f32
    raw_low: f32
    reference_high: f32
    raw_high: f32
    gain: u8


@serde
class ECConfigGain:
    value: u8


class ECEndpoint(InputEndpoint, EndpointBase.ECEndpoint):

    async def get_config(self, config: int):
        value = await self.node.get_config(self.endpoint_id, config)
        if not value:
            return {}
        if config == EndpointBase.ECConfigReadType.CALIBRATION:
            decoded: ECConfigCalibrationRaw = from_postcard(
                ECConfigCalibrationRaw, value
            )
            return {
                "reference_low": float(decoded.reference_low),
                "raw_low": float(decoded.raw_low),
                "reference_high": float(decoded.reference_high),
                "raw_high": float(decoded.raw_high),
                "gain": int(decoded.gain),
            }
        if config == EndpointBase.ECConfigReadType.RAW:
            decoded: ECConfigRaw = from_postcard(ECConfigRaw, value)
            return {"raw": float(decoded.value)}
        return {}

    async def set_config(self, config):
        if "high" in config and "low" in config:
            raise ValueError(
                "Cannot not set high and low at the same time, calibration will be wrong"
            )
        if (
            ("reference_low" in config)
            or ("raw_low" in config)
            or ("reference_high" in config)
            or ("raw_high" in config)
            or ("gain" in config)
        ):
            if (
                ("reference_low" not in config)
                or ("raw_low" not in config)
                or ("reference_high" not in config)
                or ("raw_high" not in config)
                or ("gain" not in config)
            ):
                raise ValueError(
                    "Missing configuration values. These must be set: reference_low, raw_low, reference_high, raw_high, and gain."
                )
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.ECConfigWriteType.RAW,
                ECConfigCalibrationRaw(
                    reference_low=f32(config["reference_low"]),
                    raw_low=f32(config["raw_low"]),
                    reference_high=f32(config["reference_high"]),
                    raw_high=f32(config["raw_high"]),
                    gain=u8(config["gain"]),
                ),
            )
        if "high" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.ECConfigWriteType.HIGH,
                ECConfigCalibration(value=f32(config["high"])),
            )
        if "low" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.ECConfigWriteType.LOW,
                ECConfigCalibration(value=f32(config["low"])),
            )
        if "gain" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.ECConfigWriteType.GAIN,
                ECConfigGain(value=u8(config["gain"])),
            )


@serde
class PHConfigCalibration:
    value: f32


@serde
class PHConfigRaw:
    value: f32


@serde
class PHConfigCalibrationRaw:
    reference_low: f32
    raw_low: f32
    reference_mid: f32
    raw_mid: f32
    reference_high: f32
    raw_high: f32


@serde
class PHConfigSlope:
    acid_percent: f32
    base_percent: f32
    neutral_voltage: f32


class PHEndpoint(InputEndpoint, EndpointBase.PHEndpoint):

    async def get_config(self, config: int):
        value = await self.node.get_config(self.endpoint_id, config)
        if not value:
            return {}
        if config == EndpointBase.PHConfigReadType.RAW:
            decoded: PHConfigRaw = from_postcard(PHConfigRaw, value)
            return {"raw": float(decoded.value)}
        if config == EndpointBase.PHConfigReadType.CALIBRATION:
            decoded: PHConfigCalibrationRaw = from_postcard(
                PHConfigCalibrationRaw, value
            )
            return {
                "reference_low": float(decoded.reference_low),
                "raw_low": float(decoded.raw_low),
                "reference_mid": float(decoded.reference_mid),
                "raw_mid": float(decoded.raw_mid),
                "reference_high": float(decoded.reference_high),
                "raw_high": float(decoded.raw_high),
            }
        if config == EndpointBase.PHConfigReadType.SLOPE:
            decoded: PHConfigSlope = from_postcard(PHConfigSlope, value)
            return {
                "acid_percent": float(decoded.acid_percent),
                "base_percent": float(decoded.base_percent),
                "neutral_voltage": float(decoded.neutral_voltage),
            }
        return {}

    async def set_config(self, config) -> bool:
        calibrations = 0
        if "high" in config:
            calibrations += 1
        if "low" in config:
            calibrations += 1
        if "mid" in config:
            calibrations += 1
        if calibrations > 1:
            raise ValueError(
                "Cannot not set high, low and mid at the same time, calibration will be wrong"
            )
        if "high" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.PHConfigWriteType.HIGH,
                PHConfigCalibration(value=f32(config["high"])),
            )
        if "low" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.PHConfigWriteType.LOW,
                PHConfigCalibration(value=f32(config["low"])),
            )
        if "mid" in config:
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.PHConfigWriteType.MID,
                PHConfigCalibration(value=f32(config["mid"])),
            )
        if (
            ("reference_low" in config)
            or ("raw_low" in config)
            or ("reference_mid" in config)
            or ("raw_mid" in config)
            or ("reference_high" in config)
            or ("raw_high" in config)
        ):
            if (
                ("reference_low" not in config)
                or ("raw_low" not in config)
                or ("reference_mid" not in config)
                or ("raw_mid" not in config)
                or ("reference_high" not in config)
                or ("raw_high" not in config)
            ):
                raise ValueError(
                    "Missing configuration values. These must be set: reference_low, raw_low, reference_mid, raw_mid, reference_high, and raw_high."
                )
            return await self.node.set_config(
                self.endpoint_id,
                EndpointBase.PHConfigType.MID,
                PHConfigCalibrationRaw(
                    reference_low=f32(config["reference_low"]),
                    raw_low=f32(config["raw_low"]),
                    reference_mid=f32(config["reference_mid"]),
                    raw_mid=f32(config["raw_mid"]),
                    reference_high=f32(config["reference_high"]),
                    raw_high=f32(config["raw_high"]),
                ),
            )


class VariableOutputEndpoint(EndpointBase.VariableOutputEndpoint):

    def handle_actuator_output_value(self, msg: ActuatorOutput):
        self.update(msg.value)

    async def set(self, value: float):
        self.node.send_msg(
            ActuatorOutput(endpoint_id=u8(self.endpoint_id), value=f32(value))
        )


def get_endpoint_input_class(
    endpoint_input_class: EndpointBase.EndpointInputClass,
) -> EndpointBase.InputEndpoint:
    if endpoint_input_class == EndpointBase.EndpointInputClass.Temperature:
        return TemperatureEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.Humidity:
        return HumidityEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.EC:
        return ECEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.PH:
        return PHEndpoint
    return GenericInputEndpoint


def get_endpoint_output_class(
    endpoint_output_class: EndpointBase.EndpointOutputClass,
) -> EndpointBase.OutputEndpoint:
    if endpoint_output_class == EndpointBase.EndpointOutputClass.Variable:
        return VariableOutputEndpoint
    return EndpointBase.OutputEndpoint


def get_endpoint_class(
    endpoint_class: EndpointBase.EndpointClass, endpoint_sub_class
) -> EndpointBase.Endpoint:
    if endpoint_class == EndpointClass.Input:
        return get_endpoint_input_class(endpoint_sub_class)
    if endpoint_class == EndpointClass.Output:
        return get_endpoint_output_class(endpoint_sub_class)
    return EndpointBase.Endpoint
