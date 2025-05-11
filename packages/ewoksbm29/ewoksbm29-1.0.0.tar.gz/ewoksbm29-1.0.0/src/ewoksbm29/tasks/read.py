from ewokscore import Task

from ..io.read_offline import read_scan_data_slice as read_offline
from ..io.read_online import read_scan_data_slice as read_online


class ReadScanDataSlice(
    Task,
    optional_input_names=[
        "lima_file_index",
        "dahu_to_counter_name",
        "storage_ring_current",
        "exposure_time",
        # Online:
        "scan_key",
        "retry_timeout",
        "retry_period",
        # Offline:
        "scan_file_path",
        "scan_number",
    ],
    output_names=[
        "scan_data_slice",
        "has_data",
        "lima_file_index",
        "next_lima_file_index",
    ],
):
    """Return a subset of `IntegrateParameters` for a SAXS scan index range covered
    by the lima file with index `lima_file_index`.

    Optional inputs (online & offline):
    - lima_file_index (int): Lima file index that determines the scan slice.
    - dahu_to_counter_name (dict): Map counter names to `IntegrateParameters` keys.
    - storage_ring_current (float): Storage ring current in mA.
    - exposure_time (float): Scan point exposure time in s.

    Optional inputs (online):
    - scan_key (str): Blissdata scan key (tries offline when fails).
    - retry_timeout (float): Timeout when trying to access the Lima image dataset or wait for the scan to be PREPARED.
    - retry_period (float): Period in retry loops.

    Optional inputs (offline):
    - scan_file_path (str): Bliss scan file name.
    - scan_number (str): Bliss scan number.

    Outputs:
    - scan_data_slice (dict): Subset of `IntegrateParameters` related to the scan data.
    - has_data (bool): `scan_data_slice` contains a non-empty scan data slice.
    - lima_file_index (int): The lime file index to which `scan_data_slice` belongs.
    - next_lima_file_index (int): The next Lima file index.
    """

    def run(self):
        lima_file_index: int = self.get_input_value("lima_file_index", None) or 0

        params = self.get_input_values()
        if self._has_online_parameters():
            try:
                scan_data_slice = read_online(**params)
            except Exception:
                if not self._has_offline_parameters():
                    raise
                scan_data_slice = read_offline(**params)
        elif self._has_offline_parameters():
            scan_data_slice = read_offline(**params)
        else:
            raise ValueError("Requires 'scan_key' or 'scan_file_path' + 'scan_number'")

        if not scan_data_slice:
            scan_data_slice = {"frame_ids": []}
        self.outputs.scan_data_slice = scan_data_slice

        has_data = bool(scan_data_slice["frame_ids"])
        self.outputs.has_data = has_data

        self.outputs.lima_file_index = lima_file_index
        if has_data:
            self.outputs.next_lima_file_index = lima_file_index + 1
        else:
            self.outputs.next_lima_file_index = lima_file_index

    def _has_offline_parameters(self) -> bool:
        return bool(
            self.get_input_value("scan_file_path")
            and self.get_input_value("scan_number")
        )

    def _has_online_parameters(self) -> bool:
        return bool(self.get_input_value("scan_key"))
