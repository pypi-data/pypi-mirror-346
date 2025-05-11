import logging
from functools import lru_cache

from ewokscore import Task

logger = logging.getLogger(__name__)


class AccumulateDahuJobResults(
    Task,
    input_names=["dahu_job_index", "dahu_job_id", "dahu_result"],
    output_names=["dahu_results"],
):
    """Accumulate Dahu job results with the job index as a key.

    .. code: python

        dahu_results[dahu_job_index] = {"dahu_job_id": dahu_job_id, "dahu_result": dahu_result}

    Required inputs:
    - dahu_job_index (int): Dahu job index for ordering results.
    - dahu_job_id (Optional[int]): Dahu job id (`None` means no Dahu job was executed).
    - dahu_result (Optional[dict]): Dahu result (`None` means no Dahu job was executed).

    Outputs:
    - dahu_results (Dict[int, dict]): Add the Dahu result to results from previous
                                      executions within the same workflow.
    """

    def run(self):
        ewoks_job_id = self.job_id
        dahu_results = _dahu_job_results(ewoks_job_id)
        value = {
            "dahu_job_id": self.inputs.dahu_job_id,
            "dahu_result": self.inputs.dahu_result,
        }
        dahu_results[self.inputs.dahu_job_index] = value
        self.outputs.dahu_results = dahu_results
        logger.info(
            "Accumulate dahu_job_index=%d, job_id=%d",
            self.inputs.dahu_job_id,
            self.inputs.dahu_job_index,
        )


@lru_cache(maxsize=10)
def _dahu_job_results(ewoks_job_id: str) -> dict:
    return {}
