import json
import logging
import os
import time
from typing import Optional
from typing import Tuple

import tango
from ewokscore import Task
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DahuJob(
    Task,
    optional_input_names=[
        "dahu_url",
        "dahu_parameter_file",
        "extra_dahu_parameters",
        "config_directory",
        "timeout",
        "nobackup",
        "dahu_job_index",
    ],
    output_names=["dahu_job_index", "dahu_job_id", "dahu_result"],
):
    """Ewoks task that runs a Dahu job.

    Optional inputs:
    - dahu_url (str): Tango URL of the Dahu device.
    - dahu_parameter_file (str): Dahu parameter file path (can be relative to `config_directory`).
    - extra_dahu_parameters (dict): Overwrite Dahu parameters.
    - config_directory (str): Directory of the Dahu parameter file and other config files.
    - timeout (float): Timeout waiting for the Dahu job in seconds (Default: 3600).
    - nobackup (bool): Save in the NOBACKUP directory (Default: False)).
    - dahu_job_index (int): Dahu job index for ordering results (Default: 0).

    Outputs:
    - dahu_job_index (int): Dahu job index for ordering results.
    - dahu_job_id (Optional[int]): Dahu job id (`None` means no Dahu job was executed).
    - dahu_result (Optional[dict]): Dahu result (`None` means no Dahu job was executed).
    """

    DAHU_PLUGIN: str = NotImplemented
    DAHU_INPUTS_MODEL: BaseModel = NotImplemented
    PROCESS_NAME: str = NotImplemented
    CONFIG_NAME: str = NotImplemented

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tango_proxy = None

    def run(self):
        dahu_job_index = self.get_input_value("dahu_job_index") or 0
        self.outputs.dahu_job_id, self.outputs.dahu_result = self._dahu_execute(
            dahu_job_index
        )
        self.outputs.dahu_job_index = dahu_job_index

    def dahu_parameters_initialize(self) -> dict:
        file_path = self._dahu_config_file()

        params = {}
        if file_path and os.path.exists(file_path):
            with open(file_path, "r") as f:
                params = json.load(f)

        _ = params.setdefault("plugin_name", self.DAHU_PLUGIN)

        return params

    def dahu_parameters_finalize(self, dahu_parameters: dict) -> None:
        extra_dahu_parameters = self.get_input_value("extra_dahu_parameters")
        if extra_dahu_parameters:
            dahu_parameters.update(extra_dahu_parameters)

    def dahu_parameters_save_path(self, dahu_parameters: BaseModel) -> Optional[str]:
        pass

    def _dahu_config_file(self) -> Optional[str]:
        dahu_parameter_file = self.get_input_value("dahu_parameter_file")
        if dahu_parameter_file and os.path.isabs(dahu_parameter_file):
            return dahu_parameter_file
        config_directory = self.get_input_value("config_directory")
        if not dahu_parameter_file:
            if not config_directory:
                return
            dahu_parameter_file = f"{self.CONFIG_NAME}-template.json"
        if not config_directory:
            raise ValueError("Parameter 'config_directory' is required")
        return os.path.join(config_directory, dahu_parameter_file)

    def output_filename_from_lima_filename(
        self, lima_file_path: str, extension: str
    ) -> str:
        # lima_file_path = "/data/visitor/mx2641/bm29/20250227/RAW_DATA/McoA_2F4_M311A_hplc/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A.h5"

        lima_dirname, lima_basename = os.path.split(lima_file_path)
        # lima_dirname = "/data/visitor/mx2641/bm29/20250227/RAW_DATA/McoA_2F4_M311A_hplc/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A"
        # lima_basename = "McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A.h5"

        lima_stem, _ = os.path.splitext(lima_basename)
        # lima_stem = "McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A"

        raw_dataset_dirname = os.path.dirname(lima_dirname)
        # raw_dataset_dirname = "/data/visitor/mx2641/bm29/20250227/RAW_DATA/McoA_2F4_M311A_hplc"

        processed_dataset_dirname = raw_dataset_dirname.replace(
            "RAW_DATA", self.processed_data_subdir
        )
        # processed_dataset_dirname = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc"

        return self._create_output_filename(
            processed_dataset_dirname, lima_stem, extension
        )
        # output_filename = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{self.PROCESS_NAME}/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{self.PROCESS_NAME}{extension}"

    def output_filename_from_output_filename(
        self, output_filename: str, extension: str
    ) -> str:
        # output_filename = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{PROCESS_NAME_PREV}/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{PROCESS_NAME_PREV}{extension}"

        process_dirname, process_basename = os.path.split(output_filename)
        # process_dirname = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{PROCESS_NAME_PREV}"
        # process_basename = f"McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{PROCESS_NAME_PREV}{extension}"

        if "-" in process_basename:
            lima_stem, _, _ = process_basename.rpartition("-")
        else:
            lima_stem, _ = os.path.splitext(process_basename)
        # lima_stem = "McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A"

        processed_dataset_dirname = os.path.dirname(process_dirname)
        for processed_data_subdir in ("NOBACKUP", "PROCESSED_DATA"):
            processed_dataset_dirname = processed_dataset_dirname.replace(
                processed_data_subdir, self.processed_data_subdir
            )
        # processed_dataset_dirname = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc"

        return self._create_output_filename(
            processed_dataset_dirname, lima_stem, extension
        )
        # output_filename = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{self.PROCESS_NAME}/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{self.PROCESS_NAME}{extension}"

    def _create_output_filename(
        self, processed_dataset_dirname: str, lima_stem: str, extension: str
    ) -> str:
        # processed_dataset_dirname = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc"
        # lima_stem = "McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A"

        process_dirname = os.path.join(processed_dataset_dirname, self.PROCESS_NAME)
        os.makedirs(process_dirname, exist_ok=True)
        # process_dirname = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{self.PROCESS_NAME}"

        process_basename = f"{lima_stem}-{self.PROCESS_NAME}{extension}"
        # process_basename = f"McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{self.PROCESS_NAME}{extension}"

        return os.path.join(process_dirname, process_basename)
        # output_filename = f"/data/visitor/mx2641/bm29/20250227/{self.processed_data_subdir}/McoA_2F4_M311A_hplc/{self.PROCESS_NAME}/McoA_2F4_M311A_hplc_sample_McoA_2F4_M311A-{self.PROCESS_NAME}{extension}"

    @property
    def processed_data_subdir(self):
        if self.get_input_value("nobackup", False):
            return "NOBACKUP"
        return "PROCESSED_DATA"

    @property
    def _tango_proxy(self) -> Optional[tango.DeviceProxy]:
        if self.__tango_proxy is None:
            url = self.get_input_value("dahu_url")
            if url:
                self.__tango_proxy = tango.DeviceProxy(url)
        return self.__tango_proxy

    def _dahu_execute(
        self, dahu_job_index: int
    ) -> Tuple[Optional[int], Optional[dict]]:
        logger.info("Submit Dahu job index %d", dahu_job_index)
        job_id = self._dahu_submit(dahu_job_index)
        if job_id is None:
            dahu_result = None
        else:
            dahu_result = self._dahu_get(job_id)
            logger.info("Dahu job index %d with id %s finished", dahu_job_index, job_id)
        return job_id, dahu_result

    def _dahu_submit(self, dahu_job_index: int) -> Optional[int]:
        raw_dahu_parameters = self.dahu_parameters_initialize()
        self.dahu_parameters_finalize(raw_dahu_parameters)

        model = self.DAHU_INPUTS_MODEL(**raw_dahu_parameters)
        dahu_parameters = model.model_dump(mode="json", exclude_none=True)
        payload = json.dumps(dahu_parameters, indent=4, sort_keys=True)

        dahu_parameters_save_path = self.dahu_parameters_save_path(model)
        if dahu_parameters_save_path:
            with open(dahu_parameters_save_path, "w") as f:
                f.write(payload)

        if self._tango_proxy:
            job_id = self._tango_proxy.startJob([self.DAHU_PLUGIN, payload])
            logger.info(
                "Dahu job index %d submitted: Dahu job id %s", dahu_job_index, job_id
            )
            if dahu_parameters_save_path:
                logger.info(
                    "Dahu job index %d with id %d: inputs saved in %s",
                    dahu_job_index,
                    job_id,
                    dahu_parameters_save_path,
                )
            return job_id
        else:
            logger.warning(
                "Dahu job index %d not submitted: 'dahu_url' is not provided.",
                dahu_job_index,
            )
            if dahu_parameters_save_path:
                logger.info(
                    "Dahu job index %d: inputs saved in %s",
                    dahu_job_index,
                    dahu_parameters_save_path,
                )

    def _dahu_get(self, job_id: int) -> dict:
        tango_proxy = self._tango_proxy
        timeout = self.get_input_value("timeout") or 3600
        t0 = time.time()
        while tango_proxy.getJobState(job_id) not in ("success", "failure", "aborted"):
            time.sleep(2)
            if (time.time() - t0) > timeout:
                raise TimeoutError(f"Dahu job took longer than {timeout} seconds")
        output = tango_proxy.getJobOutput(job_id)
        return json.loads(output)
