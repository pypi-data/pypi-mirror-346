# import asyncio
import base64

# import io
import logging
import sys
from pprint import pprint as pp

from pyninaapiio.api.image import get_image_history, get_image_index
from pyninaapiio.api.mount import get_equipment_mount_info, get_equipment_mount_list_devices
from pyninaapiio.api.switch import get_equipment_switch_info
from pyninaapiio.client import Client
from pyninaapiio.dataclasses import (
    CameraData,
    CameraDataModel,
    DeviceMountData,
    DeviceMountDataModel,
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
from pyninaapiio.models.device_list import DeviceList
from pyninaapiio.models.device_list_response_item import DeviceListResponseItem
from pyninaapiio.models.get_image_history_response_200 import GetImageHistoryResponse200
from pyninaapiio.models.get_image_index_bayer_pattern import GetImageIndexBayerPattern
from pyninaapiio.models.get_image_index_response_200 import GetImageIndexResponse200
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
    ):
        self._session = session
        self._client = Client(base_url=base_url)

        return None

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
    # Image
    # #########################################################################
    async def image_latest(self):
        _LOGGER.debug(f"Retrieve index of last capture")
        image_history: GetImageHistoryResponse200 = await get_image_history.asyncio(client=self._client, count=True)
        image_index_latest = image_history.response - 1

        _LOGGER.debug(f"Retrieve capture with index {image_index_latest}")
        image: GetImageIndexResponse200 = await get_image_index.asyncio(index=image_index_latest, client=self._client)
        # , debayer=True
        # )  # , bayer_pattern=GetImageIndexBayerPattern.RGGB)
        if image.success:
            decoded_data = base64.b64decode(image.response)
            _LOGGER.debug(f"Capture size: {len(decoded_data)}")

            _camera_data = CameraDataModel({"DecodedData": decoded_data})

            return CameraData(data=_camera_data)
        else:
            _LOGGER.warning(f"{image.error}")

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
    async def nina_info(self):
        try:
            _LOGGER.debug(f"Retrieve nina info")
            _nina = {
                "Mount": await self.mount_info(),
                "Switch": await self.switch_info(),
                "Camera": await self.image_latest(),
            }
            _nina_info_data = NinaDevicesDataModel(_nina)

            return NinaDevicesData(data=_nina_info_data)

        except KeyError as ke:
            _LOGGER.warning(f"Nina not connected. {ke}")
