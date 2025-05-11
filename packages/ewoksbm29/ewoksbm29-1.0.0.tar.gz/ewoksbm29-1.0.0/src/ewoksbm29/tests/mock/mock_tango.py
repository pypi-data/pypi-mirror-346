import json
from contextlib import contextmanager
from unittest.mock import MagicMock
from unittest.mock import patch


@contextmanager
def mock_dahu():
    global _JOB_STORE
    _JOB_STORE = {}

    with patch("tango.DeviceProxy") as mock_proxy_class:
        mock_proxy = MagicMock()
        mock_proxy_class.return_value = mock_proxy

        mock_proxy.startJob.side_effect = _startJob
        mock_proxy.getJobState.side_effect = _getJobState
        mock_proxy.getJobOutput.side_effect = _getJobOutput

        mock_proxy.JOB_STORE = _JOB_STORE
        yield mock_proxy


_JOB_STORE = None


def _startJob(args) -> int:
    job_id = len(_JOB_STORE) + 1
    plugin_name, json_payload = args
    parameters = json.loads(json_payload)
    output = dict(parameters)  # TODO: depends on plugin_name

    _JOB_STORE[job_id] = {
        "state": "success",
        "parameters": parameters,
        "output": output,
    }
    return job_id


def _getJobState(job_id: int) -> str:
    return _JOB_STORE.get(job_id, {}).get("state", "unknown")


def _getJobOutput(job_id: int) -> str:
    if _JOB_STORE.get(job_id, {}).get("state") == "success":
        output = _JOB_STORE[job_id]["output"]
        return json.dumps(output)
    return "null"
