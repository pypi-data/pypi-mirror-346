"""Defines the Data Classes used."""

# import math
# from dataclasses import dataclass
# from datetime import datetime
# from pprint import pprint as pp
from typing import TypedDict, Optional

from typeguard import typechecked

# from pyninaapiio.const import (
#     # CONDITION,
#     # CONDITION_PLAIN,
#     # DEEP_SKY_THRESHOLD,
#     # LIFTED_INDEX_PLAIN,
#     # LIFTED_INDEX_RANGE,
#     # LIFTED_INDEX_VALUE,
#     # MAG_DEGRATION_MAX,
#     # SEEING_MAX,
#     # WIND10M_DIRECTON,
#     # WIND10M_MAX,
#     # WIND10M_PLAIN,
#     # WIND10M_RANGE,
#     # WIND10M_VALUE,
# )


# @dataclass
# class TimeDataModel(TypedDict):
#     """Model for time data"""

#     forecast_time: datetime


# @typechecked
# class TimeData:
#     """A representation of the time data of forecasts."""

#     def __init__(self, *, data: TimeDataModel):
#         self.forecast_time = data["forecast_time"]


# class GeoLocationDataModel(TypedDict):
#     """Model for the location"""

#     latitude: float
#     longitude: float
#     elevation: float
#     timezone_info: str


# @typechecked
# class GeoLocationData:
#     """A representation of the geographic location."""

#     def __init__(self, *, data: GeoLocationDataModel):
#         self.latitude = data["latitude"]
#         self.longitude = data["longitude"]
#         self.elevation = data["elevation"]
#         self.timezone_info = data["timezone_info"]


# #########################################################################
# Mount
# #########################################################################
class DeviceMountListDataModel(TypedDict):
    items: dict


@typechecked
class DeviceMountListData:
    """A representation of the geographic location."""

    def __init__(self, *, data: DeviceMountListDataModel):
        self.items = data["items"]


class DeviceMountDataModel(TypedDict):
    # device_list_response_item

    HasSetupDialog: bool
    Id: str
    Name: str
    DisplayName: str
    Category: str
    Connected: bool
    Description: str
    DriverInfo: str
    DriverVersion: str
    SupportedActions: list
    # additional_properties: dict


@typechecked
class DeviceMountData:
    """A representation of the geographic location."""

    def __init__(self, *, data: DeviceMountDataModel):
        self.has_setup_dialog = data["HasSetupDialog"]
        self.id = data["Id"]
        self.name = data["Name"]
        self.display_name = data["DisplayName"]
        self.category = data["Category"]
        self.connected = data["Connected"]
        self.description = data["Description"]
        self.driver_info = data["DriverInfo"]
        self.driver_version = data["DriverVersion"]
        self.supported_actions = data["SupportedActions"]
        # self.additional_properties = data["additional_properties"]


class MountDataModel(TypedDict):
    connected: bool
    name: str
    display_name: str
    device_id: str
    sidereal_time: float
    right_ascension: float
    declination: float
    site_latitude: float
    site_longitude: float
    site_elevation: float


@typechecked
class MountData:
    """A representation of the geographic location."""

    def __init__(self, *, data: MountDataModel):
        self.connected = data["connected"]
        self.name = data["name"]
        self.display_name = data["display_name"]
        self.device_id = data["device_id"]
        self.sidereal_time = data["sidereal_time"]
        self.right_ascension = data["right_ascension"]
        self.declination = data["declination"]
        self.site_latitude = data["site_latitude"]
        self.site_longitude = data["site_longitude"]
        self.site_elevation = data["site_elevation"]


# #########################################################################
# Switch
# #########################################################################
class SwitchPortDataModel(TypedDict, total=False):
    # device_list_response_item

    Maximum: Optional[int]
    Minimum: Optional[int]
    StepSize: Optional[int]
    TargetValue: Optional[int]
    Id: int
    Name: str
    Description: str
    Value: float


@typechecked
class SwitchPortData:
    """A representation of the geographic location."""

    def __init__(self, *, data: SwitchPortDataModel):
        self.maximum = data.get("Maximum", None)
        self.minimum = data.get("Minimum", None)
        self.step_size = data.get("StepSize", None)
        self.target_value = data.get("TargetValue", None)
        self.id = data["Id"]
        self.name = data["Name"]
        self.description = data["Description"]
        self.value = data["Value"]


class SwitchDataModel(TypedDict, total=False):
    # device_list_response_item

    WritableSwitches: list[SwitchPortDataModel]
    ReadonlySwitches: list[SwitchPortDataModel]
    SupportedActions: list[str]
    Connected: bool
    Name: str
    DisplayName: str
    Description: str
    DriverInfo: str
    DriverVersion: str
    DeviceId: str


@typechecked
class SwitchData:
    """A representation of the geographic location."""

    def __init__(self, *, data: SwitchDataModel):
        self.writable_switches = data["WritableSwitches"]
        self.readonly_switches = data["ReadonlySwitches"]
        self.supported_actions = data["SupportedActions"]
        self.connected = data["Connected"]
        self.name = data["Name"]
        self.display_name = data["DisplayName"]
        self.description = data["Description"]
        self.driver_info = data["DriverInfo"]
        self.driver_version = data["DriverVersion"]
        self.device_id = data["DeviceId"]


# #########################################################################
# Camera
# #########################################################################
class CameraDataModel(TypedDict, total=False):
    DecodedData: bytes


class CameraData:
    def __init__(self, *, data: CameraDataModel):
        self.decoded_data = data["DecodedData"]


# #########################################################################
# N.I.N.A. Devices
# #########################################################################
class NinaDevicesDataModel(TypedDict, total=False):
    # device_list_response_item

    # Application: Optional[ApplicationData]
    Camera: Optional[CameraData]
    # Dome: Optional[DomeData]
    # FilterWheel: Optional[FilterWheelData]
    # FlatPanel: Optional[FlatPanelData]
    # Focuser: Optional[FocuserData]
    # Guider: Optional[GuiderData]
    # Image: Optional[ImageData]
    Mount: Optional[MountData]
    # Profile: Optional[ProfileData]
    # Rotator: Optional[RotatorData]
    # SafetyMonitor: Optional[SafetyMonitorData]
    # Sequence: Optional[SequenceData]
    Switch: Optional[SwitchData]


@typechecked
class NinaDevicesData:
    """A representation of the geographic location."""

    def __init__(self, *, data: NinaDevicesDataModel):
        self.mount = data["Mount"]
        self.switch = data["Switch"]
        self.camera = data["Camera"]
