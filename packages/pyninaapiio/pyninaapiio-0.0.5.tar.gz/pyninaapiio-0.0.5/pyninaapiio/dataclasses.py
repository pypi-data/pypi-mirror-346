"""Defines the Data Classes used."""

# import math
# from dataclasses import dataclass
# from datetime import datetime
# from pprint import pprint as pp
from typing import Any, Optional, TypedDict

from typeguard import typechecked

from pyninaapiio.models.guider_info_response_last_guide_step import GuiderInfoResponseLastGuideStep
from pyninaapiio.models.guider_info_response_rms_error import GuiderInfoResponseRMSError
from pyninaapiio.models.guider_info_response_state import GuiderInfoResponseState


# #########################################################################
# Application
# #########################################################################
class ApplicationDataModel(TypedDict, total=False):
    Dummy: int


class ApplicationData:
    def __init__(self, *, data: ApplicationDataModel):
        self.dummy = data.get("Dummy")


# #########################################################################
# Camera
# #########################################################################
class CameraDataModel(TypedDict, total=False):
    TargetTemp: float
    AtTargetTemp: bool
    CanSetTemperature: bool
    HasShutter: bool
    Temperature: int
    Gain: int
    DefaultGain: int
    ElectronsPerADU: int
    BinX: int
    BitDepth: int
    BinY: int
    CanSetOffset: bool
    CanGetGain: bool
    OffsetMin: int
    OffsetMax: int
    Offset: int
    DefaultOffset: int
    USBLimit: int
    IsSubSampleEnabled: bool
    CameraState: str
    XSize: int
    YSize: int
    PixelSize: int
    Battery: int
    GainMin: int
    GainMax: int
    CanSetGain: bool
    Gains: list[Any]
    CoolerOn: bool
    CoolerPower: int
    HasDewHeater: bool
    DewHeaterOn: bool
    CanSubSample: bool
    SubSampleX: int
    SubSampleY: int
    SubSampleWidth: int
    SubSampleHeight: int
    TemperatureSetPoint: int
    ReadoutModes: str
    ReadoutMode: int
    ReadoutModeForSnapImages: int
    ReadoutModeForNormalImages: int
    IsExposing: bool
    ExposureEndTime: str
    LastDownloadTime: int
    SensorType: str
    BayerOffsetX: int
    BayerOffsetY: int
    BinningModes: list[Any]
    ExposureMax: int
    ExposureMin: int
    LiveViewEnabled: bool
    CanShowLiveView: bool
    SupportedActions: str
    CanSetUSBLimit: bool
    USBLimitMin: int
    USBLimitMax: int
    Connected: bool
    Name: str
    DisplayName: str
    DeviceId: str


class CameraData:
    def __init__(self, *, data: CameraDataModel):
        self.target_temp = data.get("TargetTemp")
        self.at_target_temp = data.get("AtTargetTemp")
        self.can_set_temperature = data.get("CanSetTemperature")
        self.has_shutter = data.get("HasShutter")
        self.temperature = data.get("Temperature")
        self.gain = data.get("Gain")
        self.default_gain = data.get("DefaultGain")
        self.electrons_per_adu = data.get("ElectronsPerADU")
        self.bin_x = data.get("BinX")
        self.bit_depth = data.get("BitDepth")
        self.bin_y = data.get("BinY")
        self.can_set_offset = data.get("CanSetOffset")
        self.can_get_gain = data.get("CanGetGain")
        self.offset_min = data.get("OffsetMin")
        self.offset_max = data.get("OffsetMax")
        self.offset = data.get("Offset")
        self.default_offset = data.get("DefaultOffset")
        self.usb_limit = data.get("USBLimit")
        self.is_sub_sample_enabled = data.get("IsSubSampleEnabled")
        self.camera_state = data.get("CameraState")
        self.x_size = data.get("XSize")
        self.y_size = data.get("YSize")
        self.pixel_size = data.get("PixelSize")
        self.battery = data.get("Battery")
        self.gain_min = data.get("GainMin")
        self.gain_max = data.get("GainMax")
        self.can_set_gain = data.get("CanSetGain")
        self.gains = data.get("Gains")
        self.cooler_on = data.get("CoolerOn")
        self.cooler_power = data.get("CoolerPower")
        self.has_dew_heater = data.get("HasDewHeater")
        self.dew_heater_on = data.get("DewHeaterOn")
        self.can_sub_sample = data.get("CanSubSample")
        self.sub_sample_x = data.get("SubSampleX")
        self.sub_sample_y = data.get("SubSampleY")
        self.sub_sample_width = data.get("SubSampleWidth")
        self.sub_sample_height = data.get("SubSampleHeight")
        self.temperature_set_point = data.get("TemperatureSetPoint")
        self.readout_modes = data.get("ReadoutModes")
        self.readout_mode = data.get("ReadoutMode")
        self.readout_mode_for_snap_images = data.get("ReadoutModeForSnapImages")
        self.readout_mode_for_normal_images = data.get("ReadoutModeForNormalImages")
        self.is_exposing = data.get("IsExposing")
        self.exposure_end_time = data.get("ExposureEndTime")
        self.last_download_time = data.get("LastDownloadTime")
        self.sensor_type = data.get("SensorType")
        self.bayer_offset_x = data.get("BayerOffsetX")
        self.bayer_offset_y = data.get("BayerOffsetY")
        self.binning_modes = data.get("BinningModes")
        self.exposure_max = data.get("ExposureMax")
        self.exposure_min = data.get("ExposureMin")
        self.live_view_enabled = data.get("LiveViewEnabled")
        self.can_show_live_view = data.get("CanShowLiveView")
        self.supported_actions = data.get("SupportedActions")
        self.can_set_usb_limit = data.get("CanSetUSBLimit")
        self.usb_limit_min = data.get("USBLimitMin")
        self.usb_limit_max = data.get("USBLimitMax")
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.device_id = data.get("DeviceId")


# #########################################################################
# Focuser
# #########################################################################
class FocuserDataModel(TypedDict, total=False):
    Position: int
    StepSize: int
    Temperature: float
    IsMoving: bool
    IsSettling: bool
    TempComp: bool
    TempCompAvailable: bool
    SupportedActions: list[Any]
    Connected: bool
    Name: str
    DisplayName: str
    Description: str
    DriverInfo: str
    DriverVersion: str
    DeviceId: str


class FocuserData:
    def __init__(self, *, data: FocuserDataModel):
        self.position = data.get("Position")
        self.step_size = data.get("StepSize")
        self.temperature = data.get("Temperature")
        self.is_moving = data.get("IsMoving")
        self.is_settling = data.get("IsSettling")
        self.temp_comp = data.get("TempComp")
        self.temp_comp_available = data.get("TempCompAvailable")
        self.supported_actions = data.get("SupportedActions")
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")


# #########################################################################
# Guider
# #########################################################################
class GuiderDataModel(TypedDict, total=False):
    Connected: bool
    CanClearCalibration: bool
    CanSetShiftRate: bool
    CanGetLockPosition: bool
    PixelScale: float
    Name: str
    DisplayName: str
    Description: str
    DriverInfo: str
    DriverVersion: str
    DeviceId: str
    SupportedActions: list[Any]
    RMSError: GuiderInfoResponseRMSError
    LastGuideStep: Optional[GuiderInfoResponseLastGuideStep]
    State: GuiderInfoResponseState


class GuiderData:
    def __init__(self, *, data: GuiderDataModel):
        self.connected = data.get("Connected")
        self.can_clear_calibration = data.get("CanClearCalibration")
        self.can_set_shift_rate = data.get("CanSetShiftRate")
        self.can_get_lock_position = data.get("CanGetLockPosition")
        self.pixel_scale = data.get("PixelScale")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")
        self.supported_actions = data.get("SupportedActions")
        self.rms_error = data.get("RMSError")
        self.last_guide_step = data.get("LastGuideStep")
        self.state = data.get("State")


# #########################################################################
# Image
# #########################################################################
class ImageDataModel(TypedDict, total=False):
    DecodedData: bytes
    IndexLatest: int


class ImageData:
    def __init__(self, *, data: ImageDataModel):
        self.decoded_data = data.get("DecodedData")
        self.index_latest = data.get("IndexLatest")


# #########################################################################
# Mount
# #########################################################################
class DeviceMountListDataModel(TypedDict):
    items: dict


@typechecked
class DeviceMountListData:
    """A representation of the geographic location."""

    def __init__(self, *, data: DeviceMountListDataModel):
        self.items = data.get("items")


class DeviceMountDataModel(TypedDict):
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
        self.has_setup_dialog = data.get("HasSetupDialog")
        self.id = data.get("Id")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.category = data.get("Category")
        self.connected = data.get("Connected")
        self.description = data.get("Description")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.supported_actions = data.get("SupportedActions")
        # self.additional_properties = data.get("additional_properties")


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
        self.connected = data.get("connected")
        self.name = data.get("name")
        self.display_name = data.get("display_name")
        self.device_id = data.get("device_id")
        self.sidereal_time = data.get("sidereal_time")
        self.right_ascension = data.get("right_ascension")
        self.declination = data.get("declination")
        self.site_latitude = data.get("site_latitude")
        self.site_longitude = data.get("site_longitude")
        self.site_elevation = data.get("site_elevation")


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
        self.maximum = data.get("Maximum")
        self.minimum = data.get("Minimum")
        self.step_size = data.get("StepSize")
        self.target_value = data.get("TargetValue")
        self.id = data.get("Id")
        self.name = data.get("Name")
        self.description = data.get("Description")
        self.value = data.get("Value")


class SwitchDataModel(TypedDict, total=False):
    # device_list_response_item

    WritableSwitches: Optional[list[SwitchPortDataModel]]
    ReadonlySwitches: Optional[list[SwitchPortDataModel]]
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
        self.writable_switches = data.get("WritableSwitches")
        self.readonly_switches = data.get("ReadonlySwitches")
        self.supported_actions = data.get("SupportedActions")
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")


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
    Focuser: Optional[FocuserData]
    Guider: Optional[GuiderData]
    Image: Optional[ImageData]
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
        # self.application = data.get("Application")
        self.camera = data["Camera"]
        self.focuser = data["Focuser"]
        self.guider = data["Guider"]
        self.image = data["Image"]
        self.mount = data["Mount"]
        self.switch = data["Switch"]
