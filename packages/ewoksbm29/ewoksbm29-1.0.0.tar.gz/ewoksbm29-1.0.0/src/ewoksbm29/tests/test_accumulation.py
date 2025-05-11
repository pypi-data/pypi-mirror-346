import time

from ewokscore import Task
from ewoksppf import execute_graph


def test_accumulate_dahu_results():
    global _DAHU_JOB_COUNTER
    _DAHU_JOB_COUNTER = 0

    njobs_executed = 0

    # Check the njobs are accumulated
    i0 = 0
    njobs = 3
    inputs = [
        {"id": "job", "name": "dahu_job_index", "value": i0},
        {"id": "job", "name": "dahu_job_index_max", "value": i0 + njobs - 1},
    ]
    results = execute_graph(_WORKFLOW, pool_type="thread", inputs=inputs)

    dahu_results = {}
    for i in range(njobs):
        dahu_results[i0 + i] = {
            "dahu_job_id": i + njobs_executed,
            "dahu_result": {"value": i0 + i},
        }

    assert results == {"dahu_results": dahu_results}
    njobs_executed += njobs

    # Ensure we don't accumulate across jobs
    i0 = 10
    njobs = 3
    inputs = [
        {"id": "job", "name": "dahu_job_index", "value": i0},
        {"id": "job", "name": "dahu_job_index_max", "value": i0 + njobs - 1},
    ]
    results = execute_graph(_WORKFLOW, pool_type="thread", inputs=inputs)

    dahu_results = {}
    for i in range(njobs):
        dahu_results[i0 + i] = {
            "dahu_job_id": i + njobs_executed,
            "dahu_result": {"value": i0 + i},
        }

    assert results == {"dahu_results": dahu_results}


class _MockDahuJob(
    Task,
    input_names=["dahu_job_index", "dahu_job_index_max"],
    output_names=[
        "dahu_job_index",
        "dahu_job_id",
        "dahu_result",
        "next_dahu_job_index",
        "finished",
    ],
):
    def run(self):
        global _DAHU_JOB_COUNTER
        dahu_job_id = _DAHU_JOB_COUNTER
        _DAHU_JOB_COUNTER += 1

        dahu_job_index = self.inputs.dahu_job_index
        dahu_result = {"value": dahu_job_index}

        self.outputs.dahu_job_index = dahu_job_index
        self.outputs.dahu_job_id = dahu_job_id
        self.outputs.dahu_result = dahu_result

        self.outputs.next_dahu_job_index = dahu_job_index + 1
        self.outputs.finished = dahu_job_index >= self.inputs.dahu_job_index_max
        print(
            f"job_id={self.job_id}, dahu_job_id={dahu_job_id}, dahu_job_index={dahu_job_index}, finished={self.outputs.finished}"
        )
        time.sleep(0.1)


_DAHU_JOB_COUNTER = None

_WORKFLOW = {
    "graph": {"id": "test_accumulation"},
    "nodes": [
        {
            "id": "job",
            "task_type": "class",
            "task_identifier": f"{__name__}._MockDahuJob",
        },
        {
            "id": "accumulate",
            "task_type": "class",
            "task_identifier": "ewoksbm29.tasks.results.AccumulateDahuJobResults",
        },
    ],
    "links": [
        {
            "source": "job",
            "target": "job",
            "data_mapping": [
                {
                    "source_output": "next_dahu_job_index",
                    "target_input": "dahu_job_index",
                }
            ],
            "conditions": [{"source_output": "finished", "value": False}],
        },
        {
            "source": "job",
            "target": "accumulate",
            "data_mapping": [
                {"source_output": "dahu_job_index", "target_input": "dahu_job_index"},
                {"source_output": "dahu_job_id", "target_input": "dahu_job_id"},
                {"source_output": "dahu_result", "target_input": "dahu_result"},
            ],
        },
    ],
}
