import os
import shutil

from ..models.dahu import IntegrateParameters
from .base.dahu_ispyb import DahuJobWithIspybUpload


class DahuIntegrate(
    DahuJobWithIspybUpload,
    input_names=["scan_data_slice"],
    optional_input_names=["integrate_parameters"],
):
    """Azimuthal integration of BM29 SAXS data.

    In addition to the inputs from `DahuJobWithIspybUpload`:

    Required inputs:
    - scan_data_slice (dict): Subset of parameters related to the scan data (see `IntegrateParameters`).

    Optional inputs:
    - integrate_parameters (dict): Extra integrate parameters (see `IntegrateParameters`).
    """

    DAHU_PLUGIN = "bm29.integratemultiframe"
    DAHU_INPUTS_MODEL = IntegrateParameters
    PROCESS_NAME = "integrate"
    CONFIG_NAME = "integrate"

    def dahu_parameters_initialize(self) -> dict:
        dahu_parameters = super().dahu_parameters_initialize()
        dahu_parameters.update(self.inputs.scan_data_slice)
        return dahu_parameters

    def dahu_parameters_finalize(self, dahu_parameters: dict) -> None:
        input_file = dahu_parameters.get("input_file")
        if input_file:
            for key in ["poni_file", "mask_file"]:
                file_path = dahu_parameters.get(key)
                if not file_path:
                    continue
                dahu_parameters[key] = self._copy_config_file(file_path, input_file)

        output_file = dahu_parameters.get("output_file")
        if input_file and not output_file:
            output_file = self.output_filename_from_lima_filename(input_file, ".h5")
            dahu_parameters["output_file"] = output_file

        integrate_parameters = self.get_input_value("integrate_parameters")
        if integrate_parameters:
            dahu_parameters.update(integrate_parameters)

        super().dahu_parameters_finalize(dahu_parameters)

    def dahu_parameters_save_path(self, dahu_parameters: IntegrateParameters) -> str:
        if dahu_parameters.output_file:
            return os.path.splitext(dahu_parameters.output_file)[0] + ".json"
        return self.output_filename_from_lima_filename(
            dahu_parameters.input_file, ".json"
        )

    def _copy_config_file(self, file_path: str, lima_file_path: str) -> str:
        """
        Copy configuration files used by the processing (poni and mask file).
        """
        lima_dirname, _ = os.path.split(lima_file_path)
        raw_sample_dirname = os.path.normpath(os.path.join(lima_dirname, "..", ".."))

        processed_sample_dirname = raw_sample_dirname.replace(
            "RAW_DATA", self.processed_data_subdir
        )
        os.makedirs(processed_sample_dirname, exist_ok=True)

        basename = os.path.basename(file_path)
        file_path_copy = os.path.join(processed_sample_dirname, basename)

        if not os.path.isabs(file_path):
            config_directory = self.get_input_value("config_directory")
            if not config_directory:
                raise ValueError("Parameter 'config_directory' is required")
            file_path = os.path.join(config_directory, basename)

        if not os.path.exists(file_path_copy):
            shutil.copy(file_path, processed_sample_dirname)

        return file_path_copy
