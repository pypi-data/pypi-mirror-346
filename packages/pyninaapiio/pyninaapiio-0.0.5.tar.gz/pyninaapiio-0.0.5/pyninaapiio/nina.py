# import asyncio
import base64

# import io
import logging
import sys
from pprint import pprint as pp

from pyninaapiio.api.camera import get_equipment_camera_info
from pyninaapiio.api.focuser import get_equipment_focuser_info
from pyninaapiio.api.guider import get_equipment_guider_info
from pyninaapiio.api.image import get_image_history, get_image_index
from pyninaapiio.api.mount import get_equipment_mount_info, get_equipment_mount_list_devices
from pyninaapiio.api.switch import get_equipment_switch_info
from pyninaapiio.client import Client
from pyninaapiio.dataclasses import (
    ApplicationData,
    ApplicationDataModel,
    CameraData,
    CameraDataModel,
    # CameraData,
    # CameraDataModel,
    DeviceMountData,
    DeviceMountDataModel,
    FocuserData,
    FocuserDataModel,
    GuiderData,
    GuiderDataModel,
    ImageData,
    ImageDataModel,
    # DeviceMountListData,
    # DeviceMountListDataModel,
    MountData,
    MountDataModel,
    NinaDevicesData,
    NinaDevicesDataModel,
    SwitchData,
    # SwitchPortData,
    # SwitchPortDataModel,
    SwitchDataModel,
)
from pyninaapiio.models.camera_info import CameraInfo
from pyninaapiio.models.device_list import DeviceList

# from pyninaapiio.models.device_list_response_item import DeviceListResponseItem
from pyninaapiio.models.focuser_info import FocuserInfo
from pyninaapiio.models.get_image_history_response_200 import GetImageHistoryResponse200

# from pyninaapiio.models.get_image_index_bayer_pattern import GetImageIndexBayerPattern
from pyninaapiio.models.get_image_index_response_200 import GetImageIndexResponse200
from pyninaapiio.models.guider_info import GuiderInfo
from pyninaapiio.models.mount_info import MountInfo
from pyninaapiio.models.switch_info import SwitchInfo
from pyninaapiio.types import Response

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s (%(threadName)s) [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# async with client as client:
class NinaAPI:
    def __init__(
        self,
        # session: Optional[ClientSession] = None,
        session=None,
        base_url="http://192.168.1.234:1888/v2/api",
        # application_enabled=False,
        camera_enabled=False,
        focuser_enabled=False,
        guider_enabled=False,
        image_enabled=False,
        mount_enabled=False,
        switch_enabled=False,
    ):
        self._session = session
        self._client = Client(base_url=base_url)
        # self._application_enabled = application_enabled
        self._camera_enabled = camera_enabled
        self._focuser_enabled = focuser_enabled
        self._guider_enabled = guider_enabled
        self._image_enabled = image_enabled
        self._mount_enabled = mount_enabled
        self._switch_enabled = switch_enabled

        # Save last capture
        self._image_index_latest = -1
        self._image_data = None

        return None

    # #########################################################################
    # Application
    # #########################################################################
    # async def application_info(self):
    #     try:
    #         _LOGGER.debug(f"Retrieve application info")
    #         _application_info: Response[ApplicationInfo] = await get_equipment_application_info.asyncio(
    #             client=self._client
    #         )
    #         print(_application_info.response)
    #         _application_info_data = ApplicationDataModel(_application_info.response.to_dict())

    #         return ApplicationData(data=_application_info_data)

    #     except KeyError as ke:
    #         _LOGGER.warning(f"Application not connected. {ke}")

    # #########################################################################
    # Camera
    # #########################################################################
    async def camera_info(self):
        try:
            _LOGGER.debug(f"Retrieve camera info")
            _camera_info: Response[CameraInfo] = await get_equipment_camera_info.asyncio(client=self._client)
            print(_camera_info.response)
            _camera_info_data = CameraDataModel(_camera_info.response.to_dict())

            return CameraData(data=_camera_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Camera not connected. {ke}")

    # #########################################################################
    # Focuser
    # #########################################################################
    async def focuser_info(self):
        try:
            _LOGGER.debug(f"Retrieve focuser info")
            _focuser_info: Response[FocuserInfo] = await get_equipment_focuser_info.asyncio(client=self._client)
            print(_focuser_info.response)
            _focuser_info_data = FocuserDataModel(_focuser_info.response.to_dict())

            return FocuserData(data=_focuser_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Focuser not connected. {ke}")

    # #########################################################################
    # Guider
    # #########################################################################
    async def guider_info(self):
        try:
            _LOGGER.debug(f"Retrieve guider info")
            _guider_info: Response[GuiderInfo] = await get_equipment_guider_info.asyncio(client=self._client)
            print(_guider_info.response)
            _guider_info_data = GuiderDataModel(_guider_info.response.to_dict())

            return GuiderData(data=_guider_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Guider not connected. {ke}")

    # #########################################################################
    # Image
    # #########################################################################
    async def image_latest(self):
        _LOGGER.debug(f"Retrieve index of last capture")
        image_history: GetImageHistoryResponse200 = await get_image_history.asyncio(client=self._client, count=True)
        image_index_latest = image_history.response - 1

        if image_index_latest > self._image_index_latest:
            self._image_index_latest = image_index_latest

            _LOGGER.debug(f"Retrieve capture with index {image_index_latest}")
            image: GetImageIndexResponse200 = await get_image_index.asyncio(
                index=image_index_latest, client=self._client
            )  # , debayer=True, bayer_pattern=GetImageIndexBayerPattern.RGGB)
            if image.success:
                image_data = base64.b64decode(image.response)
                self._image_data = image_data
            else:
                _LOGGER.error(f"{image.error}")
        else:
            _LOGGER.debug(f"Returning previous capture with index {self._image_index_latest}")

        _LOGGER.debug(f"Capture Index: {self._image_index_latest}")
        _camera_data = ImageDataModel({"DecodedData": self._image_data, "IndexLatest": self._image_index_latest})
        return ImageData(data=_camera_data)

    # #########################################################################
    # Mount
    # #########################################################################
    async def mount_list_devices(self):
        items = []

        try:
            _list_devices: Response[DeviceList] = await get_equipment_mount_list_devices.asyncio(client=self._client)

            for _, device in enumerate(_list_devices.response):
                item = DeviceMountDataModel(device.to_dict())

                try:
                    items.append(DeviceMountData(data=item))
                except TypeError as ve:
                    _LOGGER.error(f"Failed to parse device data model data: {item}")
                    _LOGGER.error(ve)
        except KeyError as ke:
            _LOGGER.error(f"KeyError: {ke}")

        return items

    async def mount_info(self):
        try:
            _LOGGER.debug(f"Retrieve mount info")
            _mount_info: Response[MountInfo] = await get_equipment_mount_info.asyncio(client=self._client)
            _mount_info_data = MountDataModel(_mount_info.response.to_dict())

            return MountData(data=_mount_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Mount not connected. {ke}")

    # #########################################################################
    # Switch
    # #########################################################################
    async def switch_info(self):
        try:
            _LOGGER.debug(f"Retrieve switch info")
            _switch_info: Response[SwitchInfo] = await get_equipment_switch_info.asyncio(client=self._client)
            _switch_info_data = SwitchDataModel(_switch_info.response.to_dict())

            return SwitchData(data=_switch_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Switch not connected. {ke}")

    # #########################################################################
    # Nina
    # #########################################################################
    async def nina_info(
        self,
    ):
        try:
            _LOGGER.debug(f"Retrieve nina info")
            _nina = {
                # "Application": await self.application_info() if application_enabled else None,
                "Camera": await self.camera_info() if self._camera_enabled else None,
                "Focuser": await self.focuser_info() if self._focuser_enabled else None,
                "Guider": await self.guider_info() if self._guider_enabled else None,
                "Image": await self.image_latest() if self._image_enabled else None,
                "Mount": await self.mount_info() if self._mount_enabled else None,
                "Switch": await self.switch_info() if self._switch_enabled else None,
            }
            _nina_info_data = NinaDevicesDataModel(_nina)

            return NinaDevicesData(data=_nina_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Nina not connected. {ke}")
