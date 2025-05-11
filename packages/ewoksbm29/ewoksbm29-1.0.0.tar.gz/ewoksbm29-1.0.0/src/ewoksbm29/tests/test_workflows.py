from ..workflows import run


def test_integrate_offline(mock_dahu, offline_saxs_data, tmp_path):
    read_inputs = offline_saxs_data
    integrate_inputs = {
        "integrate_parameters": {
            "poni_file": "/tmp/calib.poni",
        },
        "dahu_url": "tango://host:port/domain/family/member",
    }
    results = run.integrate(read_inputs, integrate_inputs)

    # The order of the Dahu job ID's is undefined.
    # The order of the Dahu job index (the keys of results["dahu_results"]) is defined.
    dahu_job_ids = {
        task_outputs.pop("dahu_job_id", None)
        for task_outputs in results["dahu_results"].values()
    }

    expected = {
        "dahu_results": {
            0: {
                "dahu_result": {
                    "energy": 12.4,
                    "frame_ids": [0, 1, 2, 3, 4],
                    "input_file": str(tmp_path / "scan0001" / "lima_0000.h5"),
                    "output_file": str(
                        tmp_path / "integrate" / "lima_0000-integrate.h5"
                    ),
                    "plugin_name": "bm29.integratemultiframe",
                    "poni_file": "/tmp/calib.poni",
                },
            },
            1: {
                "dahu_result": {
                    "energy": 12.4,
                    "frame_ids": [5, 6, 7, 8, 9],
                    "input_file": str(tmp_path / "scan0001" / "lima_0001.h5"),
                    "output_file": str(
                        tmp_path / "integrate" / "lima_0001-integrate.h5"
                    ),
                    "plugin_name": "bm29.integratemultiframe",
                    "poni_file": "/tmp/calib.poni",
                },
            },
            2: {
                "dahu_result": {
                    "energy": 12.4,
                    "frame_ids": [10, 11, 12],
                    "input_file": str(tmp_path / "scan0001" / "lima_0002.h5"),
                    "output_file": str(
                        tmp_path / "integrate" / "lima_0002-integrate.h5"
                    ),
                    "plugin_name": "bm29.integratemultiframe",
                    "poni_file": "/tmp/calib.poni",
                },
            },
        }
    }

    assert results == expected

    assert dahu_job_ids == {1, 2, 3}


def test_subtract(mock_dahu, tmp_path):
    out_root = tmp_path / "sample"

    subtract_inputs = {
        "sample_file": str(out_root / "integrate" / "sample_lima_0000.h5"),
        "buffer_files": [
            str(out_root / "integrate" / "buffer1_lima_0000.h5"),
            str(out_root / "integrate" / "buffer2_lima_0000.h5"),
        ],
        "dahu_url": "tango://host:port/domain/family/member",
    }

    results = run.subtract(subtract_inputs)

    expected = {
        "dahu_results": {
            0: {
                "dahu_job_id": 1,
                "dahu_result": {
                    "sample_file": str(out_root / "integrate" / "sample_lima_0000.h5"),
                    "buffer_files": [
                        str(out_root / "integrate" / "buffer1_lima_0000.h5"),
                        str(out_root / "integrate" / "buffer2_lima_0000.h5"),
                    ],
                    "output_file": str(
                        out_root / "subtract" / "sample_lima_0000-subtract.h5"
                    ),
                    "plugin_name": "bm29.subtractbuffer",
                },
            },
        }
    }

    assert results == expected


def test_hplc_summary(mock_dahu, tmp_path):
    out_root = tmp_path / "sample"

    summary_inputs = {
        "integrated_files": [
            str(out_root / "integrate" / "sample_lima_0000.h5"),
            str(out_root / "integrate" / "sample_lima_0001.h5"),
        ],
        "dahu_url": "tango://host:port/domain/family/member",
    }

    results = run.hplc_summary(summary_inputs)

    expected = {
        "dahu_results": {
            0: {
                "dahu_job_id": 1,
                "dahu_result": {
                    "integrated_files": [
                        str(out_root / "integrate" / "sample_lima_0000.h5"),
                        str(out_root / "integrate" / "sample_lima_0001.h5"),
                    ],
                    "output_file": str(out_root / "hplc" / "sample_lima_000-hplc.h5"),
                    "plugin_name": "bm29.hplc",
                },
            }
        }
    }

    assert results == expected
