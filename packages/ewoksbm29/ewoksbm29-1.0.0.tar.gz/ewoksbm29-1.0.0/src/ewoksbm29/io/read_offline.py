import logging
import os
from typing import Optional
from typing import Tuple

import h5py
from silx.io import h5py_utils

logger = logging.getLogger(__name__)


def read_scan_data_slice(
    scan_file_path: str,
    scan_number: int,
    lima_file_index: int = 0,
    dahu_to_counter_name: Optional[dict] = None,
    storage_ring_current: Optional[float] = None,
    exposure_time: Optional[float] = None,
    **_,
) -> Optional[dict]:
    """Return a subset of `IntegrateParameters` for a SAXS scan index range covered
    by the lima file with index `lima_file_index`."""

    subscan = f"{scan_number}.1"

    with h5py_utils.File(scan_file_path, mode="r") as h5f:
        scan_entry = h5f[subscan]
        instrument = scan_entry["instrument"]

        images = _get_lima_dataset(instrument)
        if images is None:
            logger.warning(
                "scan '%s::/%s' has no Lima detector", scan_file_path, subscan
            )
            return

        virtual_sources = images.virtual_sources()
        number_of_lima_files = len(virtual_sources)
        if lima_file_index >= number_of_lima_files:
            return

        # Determine scan slice
        lima_file_path = _extract_lima_file_path(
            virtual_sources[lima_file_index], scan_file_path
        )
        start_index, stop_index = _extract_lima_slice(
            virtual_sources, lima_file_index, scan_file_path
        )

        # Slice counter data
        counter_data = {}
        if dahu_to_counter_name is None:
            dahu_to_counter_name = {}
        for dahu_name, ctr_name in dahu_to_counter_name.items():
            counter_data[dahu_name] = h5f[f"/{scan_number}.1/measurement/{ctr_name}"][
                start_index:stop_index
            ]

        # Compile scan data slice (see IntegrateParameters)
        scan_data_slice = {
            "input_file": lima_file_path,
            "frame_ids": list(range(start_index, stop_index)),
            **counter_data,
        }

        # Extract additional scan info
        energy = _get_energy(instrument)
        if energy is not None:
            scan_data_slice["energy"] = energy

        if exposure_time is None:
            exposure_time = _get_exposure_time(scan_entry)
        if exposure_time is not None:
            scan_data_slice["exposure_time"] = exposure_time

        if "storage_ring_current" not in counter_data:
            if storage_ring_current is None:
                storage_ring_current = _get_storage_ring_current(instrument)
            if storage_ring_current is not None:
                storage_ring_current = [storage_ring_current] * (
                    stop_index - start_index
                )
                scan_data_slice["storage_ring_current"] = storage_ring_current

    return scan_data_slice


def _extract_lima_file_path(vsource, scan_file_path: str) -> str:
    lima_file_path = vsource.file_name
    if os.path.isabs(lima_file_path):
        return lima_file_path
    return os.path.join(os.path.dirname(scan_file_path), lima_file_path)


def _extract_lima_slice(
    virtual_sources, lima_file_index: int, scan_file_path: str
) -> Tuple[int, int]:
    start_index = 0
    for i in range(0, lima_file_index):
        nimages = _extract_number_of_lima_images(virtual_sources[i], scan_file_path)
        start_index += nimages
    nimages = _extract_number_of_lima_images(
        virtual_sources[lima_file_index], scan_file_path
    )
    stop_index = start_index + nimages
    return start_index, stop_index


def _extract_number_of_lima_images(vsource, scan_file_path: str) -> int:
    src_space = vsource.src_space
    if src_space.shape:
        return src_space.shape[0]

    # TODO: sometimes the shape is an empty tuple
    lima_file_path = _extract_lima_file_path(vsource, scan_file_path)
    with h5py_utils.File(lima_file_path) as f:
        return len(f[vsource.dset_name])


def _get_lima_dataset(instrument: h5py.Group) -> Optional[h5py.Dataset]:
    for name in instrument:
        h5item = instrument[name]
        if not isinstance(h5item, h5py.Group):
            continue
        if "type" not in h5item:
            continue
        stype = h5item["type"][()]
        try:
            stype = stype.decode()
        except AttributeError:
            pass
        if stype != "lima":
            continue
        if "image" not in h5item:
            continue
        image = h5item["image"]
        if not image.is_virtual:
            continue
        return image


def _get_energy(instrument: h5py.Group) -> Optional[float]:
    """Energy in keV"""
    try:
        return instrument["positioners_start"]["energy"][()]
    except KeyError:
        return None


def _get_exposure_time(scan_entry: h5py.Group) -> Optional[float]:
    """Exposure time in seconds"""
    try:
        return scan_entry["scan_parameters"]["count_time"][()]
    except KeyError:
        return None


def _get_storage_ring_current(instrument: h5py.Group) -> Optional[float]:
    """Storage ring current in mA"""
    source = _get_nxsource(instrument)
    if not source:
        return None
    try:
        return source["current"][()]
    except KeyError:
        return None


def _get_nxsource(instrument: h5py.Group) -> Optional[h5py.Group]:
    for name in instrument:
        h5item = instrument[name]
        if not isinstance(h5item, h5py.Group):
            continue
        if h5item.attrs.get("NXsource"):
            return h5item
