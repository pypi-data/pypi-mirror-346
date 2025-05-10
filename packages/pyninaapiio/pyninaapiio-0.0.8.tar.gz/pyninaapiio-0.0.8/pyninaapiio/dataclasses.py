"""Defines the Data Classes used."""

# import math
# from dataclasses import dataclass
# from datetime import datetime
# from pprint import pprint as pp
from typing import Any, Optional, TypedDict

from typeguard import typechecked

from pyninaapiio.models.fw_info_response_available_filters_item import FWInfoResponseAvailableFiltersItem
from pyninaapiio.models.fw_info_response_selected_filter import FWInfoResponseSelectedFilter
from pyninaapiio.models.guider_info_response_last_guide_step import GuiderInfoResponseLastGuideStep
from pyninaapiio.models.guider_info_response_rms_error import GuiderInfoResponseRMSError
from pyninaapiio.models.guider_info_response_state import GuiderInfoResponseState
from pyninaapiio.models.mount_info_response_alignment_mode import MountInfoResponseAlignmentMode
from pyninaapiio.models.mount_info_response_coordinates import MountInfoResponseCoordinates
from pyninaapiio.models.mount_info_response_equatorial_system import MountInfoResponseEquatorialSystem
from pyninaapiio.models.mount_info_response_primary_axis_rates_item import MountInfoResponsePrimaryAxisRatesItem
from pyninaapiio.models.mount_info_response_secondary_axis_rates_item import MountInfoResponseSecondaryAxisRatesItem
from pyninaapiio.models.mount_info_response_side_of_pier import MountInfoResponseSideOfPier
from pyninaapiio.models.mount_info_response_tracking_modes_item import MountInfoResponseTrackingModesItem
from pyninaapiio.models.mount_info_response_tracking_rate import MountInfoResponseTrackingRate


# #########################################################################
# Application
# #########################################################################
class ApplicationDataModel(TypedDict, total=False):
    Connected: bool
    Version: str


class ApplicationData:
    def __init__(self, *, data: ApplicationDataModel):
        self.version = data.get("Version")
        self.connected = data.get("Connected")


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
# FilterWheel
# #########################################################################
class FilterWheelDataModel(TypedDict, total=False):
    AvailableFilters: list[FWInfoResponseAvailableFiltersItem]
    Connected: bool
    Description: str
    DeviceId: str
    DisplayName: str
    DriverInfo: str
    DriverVersion: str
    IsMoving: bool
    Name: str
    SelectedFilter: FWInfoResponseSelectedFilter
    SupportedActions: list[Any]


class FilterWheelData:
    def __init__(self, *, data: FilterWheelDataModel):
        self.available_filters = data.get("AvailableFilters")
        self.connected = data.get("Connected")
        self.description = data.get("Description")
        self.device_id = data.get("DeviceId")
        self.display_name = data.get("DisplayName")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.is_moving = data.get("IsMoving")
        self.name = data.get("Name")
        self.selected_filter = data.get("SelectedFilter")
        self.supported_actions = data.get("SupportedActions")

    @property
    def selected_filter_id(self) -> int:
        return self.selected_filter.get("Id")

    @property
    def selected_filter_name(self) -> str:
        return self.selected_filter.get("Name")


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

    @property
    def rms_error_ra_arcsec(self) -> float:
        return self.rms_error.get("RA").get("Arcseconds")

    @property
    def rms_error_ra_peak_arcsec(self) -> float:
        return self.rms_error.get("PeakRA").get("Arcseconds")

    @property
    def rms_error_dec_arcsec(self) -> float:
        return self.rms_error.get("Dec").get("Arcseconds")

    @property
    def rms_error_dec_peak_arcsec(self) -> float:
        return self.rms_error.get("PeakDec").get("Arcseconds")

    @property
    def rms_error_total_arcsec(self) -> float:
        return self.rms_error.get("Total").get("Arcseconds")


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


class MountDataModel(TypedDict, total=False):
    Connected: bool
    Name: str
    DisplayName: str
    AlignmentMode: MountInfoResponseAlignmentMode | Any
    Altitude: float
    AltitudeString: str
    AtHome: bool
    AtPark: bool
    Azimuth: float
    AzimuthString: str
    CanFindHome: bool
    CanMovePrimaryAxis: bool
    CanMoveSecondaryAxis: bool
    CanPark: bool
    CanPulseGuide: bool
    CanSetDeclinationRate: bool
    CanSetPark: bool
    CanSetPierSide: bool
    CanSetRightAscensionRate: bool
    CanSetTrackingEnabled: bool
    CanSlew: bool
    Coordinates: MountInfoResponseCoordinates | Any
    Declination: float
    DeclinationString: str
    DeviceId: str
    EquatorialSystem: MountInfoResponseEquatorialSystem | Any
    GuideRateDeclinationArcsecPerSec: int | Any
    GuideRateRightAscensionArcsecPerSec: int | Any
    HasUnknownEpoch: bool
    HoursToMeridianString: str
    IsPulseGuiding: bool
    PrimaryAxisRates: MountInfoResponsePrimaryAxisRatesItem | Any
    RightAscension: float
    RightAscensionString: str
    SecondaryAxisRates: MountInfoResponseSecondaryAxisRatesItem | Any
    SideOfPier: MountInfoResponseSideOfPier | Any
    SiderealTime: float
    SiderealTimeString: str
    SiteElevation: float
    SiteLatitude: float
    SiteLongitude: float
    Slewing: bool
    SupportedActions: list[str]
    TimeToMeridianFlip: float
    TimeToMeridianFlipString: str
    TrackingEnabled: bool
    TrackingModes: MountInfoResponseTrackingModesItem | Any
    TrackingRate: MountInfoResponseTrackingRate | Any
    UTCDate: str


@typechecked
class MountData:
    """A representation of the geographic location."""

    def __init__(self, *, data: MountDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.alignment_mode = data.get("AlignmentMode")
        self.altitude = data.get("Altitude")
        self.altitude_string = data.get("AltitudeString")
        self.at_home = data.get("AtHome")
        self.at_park = data.get("AtPark")
        self.azimuth = data.get("Azimuth")
        self.azimuth_string = data.get("AzimuthString")
        self.can_find_home = data.get("CanFindHome")
        self.can_move_primary_axis = data.get("CanMovePrimaryAxis")
        self.can_move_secondary_axis = data.get("CanMoveSecondaryAxis")
        self.can_park = data.get("CanPark")
        self.can_pulse_guide = data.get("CanPulseGuide")
        self.can_set_declination_rate = data.get("CanSetDeclinationRate")
        self.can_set_park = data.get("CanSetPark")
        self.can_set_pier_side = data.get("CanSetPierSide")
        self.can_set_right_ascension_rate = data.get("CanSetRightAscensionRate")
        self.can_set_tracking_enabled = data.get("CanSetTrackingEnabled")
        self.can_slew = data.get("CanSlew")
        self.coordinates = data.get("Coordinates")
        self.declination = data.get("Declination")
        self.declination_string = data.get("DeclinationString")
        self.device_id = data.get("DeviceId")
        self.equatorial_system = data.get("EquatorialSystem")
        self.guide_rate_declination_arcsec_per_sec = data.get("GuideRateDeclinationArcsecPerSec")
        self.guide_rate_right_ascension_arcsec_per_sec = data.get("GuideRateRightAscensionArcsecPerSec")
        self.has_unknown_epoch = data.get("HasUnknownEpoch")
        self.hours_to_meridian_string = data.get("HoursToMeridianString")
        self.is_pulse_guiding = data.get("IsPulseGuiding")
        self.primary_axis_rates = data.get("PrimaryAxisRates")
        self.right_ascension = data.get("RightAscension")
        self.right_ascension_string = data.get("RightAscensionString")
        self.secondary_axis_rates = data.get("SecondaryAxisRates")
        self.side_of_pier = data.get("SideOfPier")
        self.sidereal_time = data.get("SiderealTime")
        self.sidereal_time_string = data.get("SiderealTimeString")
        self.site_elevation = data.get("SiteElevation")
        self.site_latitude = data.get("SiteLatitude")
        self.site_longitude = data.get("SiteLongitude")
        self.slewing = data.get("Slewing")
        self.supported_actions = data.get("SupportedActions")
        self.time_to_meridian_flip = data.get("TimeToMeridianFlip")
        self.time_to_meridian_flip_string = data.get("TimeToMeridianFlipString")
        self.tracking_enabled = data.get("TrackingEnabled")
        self.tracking_modes = data.get("TrackingModes")
        self.tracking_rate = data.get("TrackingRate")
        self.utc_date = data.get("UTCDate")

    @property
    def coordinates_ra(self) -> float:
        print(self.coordinates)
        return self.coordinates.get("RA")

    @property
    def coordinates_ra_str(self) -> str:
        return self.coordinates.get("RAString")

    @property
    def coordinates_dec(self) -> float:
        return self.coordinates.get("Dec")

    @property
    def coordinates_dec_str(self) -> str:
        return self.coordinates.get("DecString")


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

    Application: Optional[ApplicationData]
    Camera: Optional[CameraData]
    # Dome: Optional[DomeData]
    FilterWheel: Optional[FilterWheelData]
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
        self.application = data.get("Application")
        self.camera = data["Camera"]
        self.filterwheel = data["FilterWheel"]
        self.focuser = data["Focuser"]
        self.guider = data["Guider"]
        self.image = data["Image"]
        self.mount = data["Mount"]
        self.switch = data["Switch"]
