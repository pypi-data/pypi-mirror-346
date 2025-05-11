from ..models import dahu
from ..models import ispyb


def test_ispyb_metadata():
    model = ispyb.ISPyBMetadata(
        experiment_id=1234,
        run_number=10,
        proposal_name="mx2654",
        proposal_session_name="20250226",
        beamline="bm29",
        sample_name="N_20deg_sc",
    )
    expected = {
        "experiment_id": 1234,
        "run_number": 10,
        "pyarch": "/data/pyarch/2025/bm29/mx2654/20250226/N_20deg_sc",
    }
    assert model.ispyb_parameters == expected


def test_integrate_parameters():
    _ = dahu.IntegrateParameters(
        plugin_name="bm29.integratemultiframe",
        input_file="/tmp/sample_lima0000.h5",
        poni_file="/tmp/test.poni",
        energy=12.4,
    )


def test_subtract_parameters():
    _ = dahu.SubtractParameters(
        plugin_name="bm29.subtractbuffer",
        sample_file="/tmp/sample_lima0000.h5",
        buffer_files=["/tmp/buffer_lima0000.h5", "/tmp/buffer_lima0001.h5"],
    )


def test_hplc_summary_parameters():
    _ = dahu.HplcSummaryParameters(
        plugin_name="bm29.hplc",
        integrated_files=["/tmp/sample_lima0000.h5", "/tmp/sample_lima0001.h5"],
    )
