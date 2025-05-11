import os
from typing import Optional

from ..models.dahu import HplcSummaryParameters
from .base.dahu_ispyb import DahuJobWithIspybUpload


class DahuHplcSummary(
    DahuJobWithIspybUpload,
    input_names=["integrated_files"],
    optional_input_names=["hplc_summary_parameters"],
):
    """Rebuild the complete chromatogram with basic analysis.

    In addition to the inputs from `DahuJobWithIspybUpload`:

    Required inputs:
    - integrated_files (List[str]): Azimuthally integrated SAXS data.

    Optional inputs:
    - hplc_summary_parameters (dict): Extra subtract parameters (see `HplcSummaryParameters`).
    """

    DAHU_PLUGIN = "bm29.hplc"
    DAHU_INPUTS_MODEL = HplcSummaryParameters
    PROCESS_NAME = "hplc"
    CONFIG_NAME = "hplc-summary"

    def dahu_parameters_initialize(self) -> dict:
        dahu_parameters = super().dahu_parameters_initialize()

        integrated_files = self.get_input_value("integrated_files")
        if integrated_files:
            dahu_parameters["integrated_files"] = integrated_files

        return dahu_parameters

    def dahu_parameters_finalize(self, dahu_parameters: dict) -> None:
        integrated_files = self.get_input_value("integrated_files")
        output_file = dahu_parameters.get("output_file")
        if integrated_files and not output_file:
            _, ext = os.path.splitext(integrated_files[0])
            output_filename = (
                os.path.commonprefix(integrated_files) + ext
            )  # does not exist
            output_file = self.output_filename_from_output_filename(
                output_filename, ".h5"
            )
            dahu_parameters["output_file"] = output_file

        hplc_summary_parameters = self.get_input_value("hplc_summary_parameters")
        if hplc_summary_parameters:
            dahu_parameters.update(hplc_summary_parameters)

        super().dahu_parameters_finalize(dahu_parameters)

    def dahu_parameters_save_path(
        self, dahu_parameters: HplcSummaryParameters
    ) -> Optional[str]:
        if dahu_parameters.output_file:
            return os.path.splitext(dahu_parameters.output_file)[0] + ".json"
        if dahu_parameters.integrated_files:
            return self.output_filename_from_output_filename(
                dahu_parameters.integrated_files[0], ".json"
            )
