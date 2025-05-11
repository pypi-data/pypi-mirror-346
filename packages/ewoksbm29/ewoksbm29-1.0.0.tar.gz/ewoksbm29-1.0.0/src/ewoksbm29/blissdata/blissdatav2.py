import time
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

from blissdata.beacon.data import BeaconData
from blissdata.redis_engine.exceptions import NoScanAvailable
from blissdata.redis_engine.scan import Scan
from blissdata.redis_engine.scan import ScanState
from blissdata.redis_engine.store import DataStore
from blissdata.streams.base import Stream


def wait_scan_prepared(scan_key: str, retry_timeout: float) -> Scan:
    """Returns the blissdata scan object."""
    redis_url = BeaconData().get_redis_data_db()
    data_store = DataStore(redis_url)
    scan = data_store.load_scan(scan_key)
    t0 = time.time()
    while scan.state < ScanState.PREPARED:
        if (time.time() - t0) >= retry_timeout:
            raise TimeoutError(
                f"Scan {scan_key} is not PREPARED {retry_timeout} seconds"
            )
        scan.update(block=False)
    return scan


def get_streams_with_lima(
    scan, counter_names: List[str]
) -> Tuple[Optional[Stream], Dict[str, Stream]]:
    """Return the Lima stream and counter streams"""
    lima_stream = None
    counter_streams = dict()

    for name, stream in scan.streams.items():
        if (
            stream.event_stream.encoding["type"] == "json"
            and "lima" in stream.info["format"]
        ):
            lima_stream = stream

        elif name.split(":")[-1] in counter_names:
            counter_streams[name.split(":")[-1]] = stream

    return lima_stream, counter_streams


def iter_scans(timeout: float = 1) -> Generator[Scan, None, None]:
    redis_url = BeaconData().get_redis_data_db()
    data_store = DataStore(redis_url)

    since = data_store.get_last_scan_timetag()

    while True:
        try:
            since, scan_key = data_store.get_next_scan(since=since, timeout=timeout)
        except NoScanAvailable:
            continue
        scan = data_store.load_scan(scan_key)
        yield scan
