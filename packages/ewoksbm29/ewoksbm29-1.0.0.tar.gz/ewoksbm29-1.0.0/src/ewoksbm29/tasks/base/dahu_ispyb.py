from ...models.ispyb import ISPyBMetadata
from .dahu import DahuJob


class DahuJobWithIspybUpload(
    DahuJob,
    optional_input_names=["ispyb_metadata", "ispyb_url"],
):
    """Ewoks task that runs a Dahu job with uploading to Ipysb.

    In addition to the inputs from `DahuJob`:

    Optional inputs:
    - ispyb_metadata (dict): Scan metadata (see `ISPyBMetadata`).
    - ispyb_url (str): WDSL end-point of the Ispyb SOAP service.
    """

    def dahu_parameters_initialize(self) -> dict:
        dahu_parameters = super().dahu_parameters_initialize()

        ispyb_metadata = self.get_input_value("ispyb_metadata")
        if ispyb_metadata:
            ispyb_metadata = ISPyBMetadata(**ispyb_metadata)
            self._add_ispyb_metadata(dahu_parameters, ispyb_metadata)

        return dahu_parameters

    def _add_ispyb_metadata(
        self, dahu_parameters: dict, ispyb_metadata: ISPyBMetadata
    ) -> None:
        dahu_parameters["ispyb"] = ispyb_metadata.ispyb_parameters

        ispyb_url = self.get_input_value("ispyb_url")
        if ispyb_url:
            dahu_parameters["ispyb"]["url"] = ispyb_url

    def dahu_parameters_finalize(self, dahu_parameters: dict) -> None:
        if not self.missing_inputs.ispyb_url and not self.inputs.ispyb_url:
            # Ispyb upload is explicitly disabled
            if "ispyb" in dahu_parameters:
                _ = dahu_parameters["ispyb"].pop("url", None)

        super().dahu_parameters_finalize(dahu_parameters)
