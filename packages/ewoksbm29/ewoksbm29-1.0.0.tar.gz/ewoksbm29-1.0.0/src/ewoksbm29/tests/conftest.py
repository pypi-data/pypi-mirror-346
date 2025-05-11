import pytest

from .mock import hdf5_data
from .mock import mock_tango


@pytest.fixture
def mock_dahu():
    with mock_tango.mock_dahu() as mock_proxy:
        yield mock_proxy


@pytest.fixture
def offline_saxs_data(tmp_path) -> dict:
    return hdf5_data.offline_saxs_data(str(tmp_path))
