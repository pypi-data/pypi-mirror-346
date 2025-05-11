from importlib.metadata import version

from packaging.version import Version

_BLISSDATA_VERSION = Version(version("blissdata"))

# bliss 2.0  -> blissdata 1.0.x
# bliss 2.1  -> blissdata 1.1.x
# master     -> blissdata 2.0.x

if _BLISSDATA_VERSION >= Version("2.0.0rc1"):
    from .blissdatav2 import get_streams_with_lima  # noqa F401
    from .blissdatav2 import iter_scans  # noqa F401
    from .blissdatav2 import wait_scan_prepared  # noqa F401
else:
    from .blissdatav1 import get_streams_with_lima  # noqa F401
    from .blissdatav1 import iter_scans  # noqa F401
    from .blissdatav1 import wait_scan_prepared  # noqa F401
