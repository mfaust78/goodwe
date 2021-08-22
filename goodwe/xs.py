import logging
from typing import Callable

from goodwe.dt import DT
from goodwe.processor import ProcessorResult, AbstractDataProcessor
from goodwe.protocol import ProtocolCommand
from goodwe.utils import *

logger = logging.getLogger(__name__)


class GoodWeXSProcessor(AbstractDataProcessor):

    def process_data(self, data: bytes) -> ProcessorResult:
        """Process the data provided by the GoodWe XS inverter and return ProcessorResult"""
        sensors = DT._map_response(data[5:-2], DT.sensors())

        return ProcessorResult(
            date=sensors['timestamp'],
            volts_dc=sensors['vpv1'],
            current_dc=sensors['ipv1'],
            volts_ac=sensors['vgrid1'],
            current_ac=sensors['igrid1'],
            frequency_ac=sensors['fgrid1'],
            generation_today=sensors['e_day'],
            generation_total=sensors['e_total'],
            rssi=self._get_rssi(data), # this is just response checksum
            operational_hours=sensors['h_total'],
            temperature=sensors['temperature'],
            power=sensors['ppv'],
            status=sensors['work_mode_label'])

    def _get_rssi(self, data) -> float:
        """Retrieve rssi from GoodWe data"""
        with io.BytesIO(data) as buffer:
            return read_bytes2(buffer, 149)

    def get_runtime_data_command(self) -> ProtocolCommand:
        """Answer protocol command for reading runtime data"""
        return DT._READ_DEVICE_RUNNING_DATA
