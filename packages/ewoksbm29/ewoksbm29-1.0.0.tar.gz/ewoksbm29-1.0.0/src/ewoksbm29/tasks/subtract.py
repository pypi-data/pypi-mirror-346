import os

from ..models.dahu import SubtractParameters
from .base.dahu_ispyb import DahuJobWithIspybUpload


class DahuSubtract(
    DahuJobWithIspybUpload,
    input_names=["sample_file", "buffer_files"],
    optional_input_names=["subtract_parameters"],
):
    """Subtract average integrated buffer signal from the sample signal.

    In addition to the inputs from `DahuJobWithIspybUpload`:

    Required inputs:
    - sample_file (str): Azimuthally integrated SAXS data.
    - buffer_files (List[str]): Azimuthally integrated SAXS data of the buffer.

    Optional inputs:
    - subtract_parameters (dict): Extra subtract parameters (see `SubtractParameters`).
    """

    DAHU_PLUGIN = "bm29.subtractbuffer"
    DAHU_INPUTS_MODEL = SubtractParameters
    PROCESS_NAME = "subtract"
    CONFIG_NAME = "subtract"

    def dahu_parameters_initialize(self) -> dict:
        dahu_parameters = super().dahu_parameters_initialize()

        sample_file = self.get_input_value("sample_file")
        if sample_file:
            dahu_parameters["sample_file"] = sample_file

        buffer_files = self.get_input_value("buffer_files")
        if buffer_files:
            dahu_parameters["buffer_files"] = buffer_files

        return dahu_parameters

    def dahu_parameters_finalize(self, dahu_parameters: dict) -> None:
        sample_file = dahu_parameters.get("sample_file")
        output_file = dahu_parameters.get("output_file")
        if sample_file and not output_file:
            output_file = self.output_filename_from_output_filename(sample_file, ".h5")
            dahu_parameters["output_file"] = output_file

        subtract_parameters = self.get_input_value("subtract_parameters")
        if subtract_parameters:
            dahu_parameters.update(subtract_parameters)

        super().dahu_parameters_finalize(dahu_parameters)

    def dahu_parameters_save_path(self, dahu_parameters: SubtractParameters) -> str:
        if dahu_parameters.output_file:
            return os.path.splitext(dahu_parameters.output_file)[0] + ".json"
        return self.output_filename_from_lima_filename(
            dahu_parameters.sample_file, ".json"
        )
