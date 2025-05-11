from typing import Dict
from typing import List
from typing import Union

from celery.result import AsyncResult
from ewoksjob.client import submit
from ewoksppf import execute_graph
from ewoksutils.task_utils import task_inputs


def integrate(
    read_inputs: dict, integrate_inputs: dict, remote: bool = False
) -> Union[Dict[int, dict], AsyncResult]:
    inputs = task_inputs(task_identifier="ReadScanDataSlice", inputs=read_inputs)
    inputs += task_inputs(task_identifier="DahuIntegrate", inputs=integrate_inputs)
    return _execute("integrate", inputs, remote=remote)


def subtract(subtract_inputs: dict, remote: bool = False) -> None:
    inputs = task_inputs(task_identifier="DahuSubtract", inputs=subtract_inputs)
    return _execute("subtract", inputs, remote=remote)


def hplc_summary(summary_inputs: dict, remote: bool = False) -> None:
    inputs = task_inputs(task_identifier="DahuHplcSummary", inputs=summary_inputs)
    return _execute("hplc_summary", inputs, remote=remote)


def _execute(workflow: str, inputs: List[dict], remote: bool = False):
    args = (workflow,)
    kwargs = {
        "inputs": inputs,
        "engine": "ppf",
        "pool_type": "thread",
        # "max_workers": 3,
        "load_options": {"root_module": "ewoksbm29.workflows"},
    }
    if remote:
        return submit(args=args, kwargs=kwargs)
    else:
        return execute_graph(*args, **kwargs)
