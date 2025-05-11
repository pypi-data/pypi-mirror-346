import logging
import os
import time
from typing import Optional

from blissdata.redis_engine.scan import ScanState
from silx.io import h5py_utils
from silx.utils.retry import RetryTimeoutError

from ..blissdata import get_streams_with_lima
from ..blissdata import wait_scan_prepared

logger = logging.getLogger(__name__)


def read_scan_data_slice(
    scan_key: str,
    lima_file_index: int = 0,
    retry_timeout: int = 10,
    retry_period: int = 1,
    dahu_to_counter_name: Optional[dict] = None,
    storage_ring_current: Optional[float] = None,
    exposure_time: Optional[float] = None,
    **_,
) -> Optional[dict]:
    """Return a subset of `IntegrateParameters` for a SAXS scan index range covered
    by the lima file with index `lima_file_index`."""

    # Wait for scan to be PREPARED
    scan = wait_scan_prepared(scan_key, retry_timeout)

    # Get Blissdata streams
    if dahu_to_counter_name is None:
        dahu_to_counter_name = {}
    counter_to_dahu_name = {v: k for k, v in dahu_to_counter_name.items()}
    lima_stream, counter_streams = get_streams_with_lima(
        scan, list(counter_to_dahu_name)
    )
    if lima_stream is None:
        logger.warning("scan '%s' has no Lima stream", scan_key)
        return
    lima_info = lima_stream.info["lima_info"]

    # Wait until the next lima file appears on disk or the scan is finished
    next_lima_file_path = lima_info["file_path"] % (lima_file_index + 1)
    while scan.state < ScanState.CLOSED and not os.path.exists(next_lima_file_path):
        time.sleep(retry_period)
        scan.update(block=False)

    # When the scan is finished and the lima file does not exist, no more data is expected
    lima_file_path = lima_info["file_path"] % lima_file_index
    if scan.state >= ScanState.CLOSED and not os.path.exists(lima_file_path):
        return

    # Get number of Lima images
    logger.info("Select Lima file: %s", lima_file_path)
    lima_data_path = lima_info["data_path"]
    nimages = _wait_lima_images_accessible(
        lima_file_path, lima_data_path, retry_timeout, retry_period
    )
    if nimages == 0:
        if scan.state < ScanState.CLOSED:
            logger.warning("Lima file '%s' has no images", lima_file_path)
        return

    # Determine scan slice
    frame_per_file = lima_info["frame_per_file"]
    start_index = lima_file_index * frame_per_file
    stop_index = start_index + nimages

    # Slice counter data
    if not counter_streams:
        counter_data = {}
    elif start_index == stop_index:
        counter_data = {dahu_name: [] for dahu_name in dahu_to_counter_name}
    else:
        if scan.state >= ScanState.CLOSED:
            npoints = min(len(stream) for stream in counter_streams.values())
            stop_index = min(stop_index, npoints)

        counter_data = {
            counter_to_dahu_name[ctr_name]: stream[start_index:stop_index].tolist()
            for ctr_name, stream in counter_streams.items()
        }

    # Compile scan data slice (see IntegrateParameters)
    scan_data_slice = {
        "input_file": lima_file_path,
        "frame_ids": list(range(start_index, stop_index)),
        **counter_data,
    }

    # Extract additional scan info
    scan_info = scan.info

    energy = _get_energy(scan_info)
    if energy is not None:
        scan_data_slice["energy"] = energy

    if exposure_time is None:
        exposure_time = _get_exposure_time(scan_info)
    if exposure_time is not None:
        scan_data_slice["exposure_time"] = exposure_time

    if "storage_ring_current" not in counter_data:
        if storage_ring_current is None:
            storage_ring_current = _get_storage_ring_current(scan_info)

        if storage_ring_current is not None:
            storage_ring_current = [storage_ring_current] * (stop_index - start_index)
            scan_data_slice["storage_ring_current"] = storage_ring_current

    return scan_data_slice


def _wait_lima_images_accessible(
    lima_file_path: str, lima_data_path: str, retry_timeout: float, retry_period: float
) -> int:
    """Returns number of lima images in the `"{lima_file_path}::{lima_data_path}"` dataset."""
    try:
        with h5py_utils.open_item(
            lima_file_path,
            lima_data_path,
            mode="r",
            retry_timeout=retry_timeout,
            retry_period=retry_period,
        ) as images:
            return len(images)
    except RetryTimeoutError:
        return 0


def _get_energy(scan_info: dict) -> Optional[float]:
    """Energy in keV"""
    try:
        return scan_info["positioners"]["positioners_start"]["energy"]
    except KeyError:
        return None


def _get_exposure_time(scan_info) -> Optional[float]:
    """Exposure time in seconds"""
    return scan_info.get("count_time")


def _get_storage_ring_current(scan_info: dict) -> Optional[float]:
    """Storage ring current in mA"""
    instrument = scan_info.get("instrument", {})
    for item in instrument.values():
        if not isinstance(item, dict):
            continue
        if item.get("@NX_class") == "NXsource":
            return item.get("current")
