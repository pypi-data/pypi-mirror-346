from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import HttpUrl


class SampleMetadata(BaseModel):
    # Dahu plugins: bm29.common.Sample
    name: Optional[str] = None
    description: Optional[str] = None  # protein description like "Bovine Serum Albumin"
    buffer: Optional[str] = None  # description of buffer, pH, ...
    concentration: Optional[float] = None  # in mg/mL
    hplc: Optional[str] = None  # column name and chromatography conditions
    temperature: Optional[float] = None  # Exposure temperature
    temperature_env: Optional[float] = None  # Storage temperature


class IspybParameters(BaseModel):
    # Dahu plugins: bm29.common.Ispyb
    url: Optional[HttpUrl] = None  # WDSL end-point of the Ispyb SOAP service
    pyarch: Optional[str] = None  # archive directory
    experiment_id: Optional[int] = None
    run_number: Union[int, List[int], None] = None


class DahuParameters(BaseModel):
    plugin_name: str


class DahuWithIpybUploadParameters(DahuParameters):
    ispyb: Optional[IspybParameters] = None


class IntegrateParameters(DahuWithIpybUploadParameters):
    # Dahu plugins: bm29.integrate.IntegrateMultiframe.setup
    plugin_name: Literal["bm29.integratemultiframe"]
    input_file: str  # Lima file name
    poni_file: str
    energy: float  # in keV
    output_file: Optional[str] = None  # Result file name
    max_frame: Optional[int] = None
    frame_ids: Optional[List[int]] = None  # Scan point indices
    timestamps: Optional[List[float]] = None
    monitor_values: Union[float, List[float], None] = None
    storage_ring_current: Optional[List[float]] = None
    exposure_time: Optional[float] = None  # seconds
    normalization_factor: Optional[float] = None
    mask_file: Optional[str] = None
    npt: Optional[int] = None  # Number of radial bins
    fidelity_abs: Optional[float] = None
    fidelity_rel: Optional[float] = None
    hplc_mode: Optional[Literal[0, 1]] = None
    timeout: Optional[int] = None
    sample: Optional[SampleMetadata] = None


class SubtractParameters(DahuWithIpybUploadParameters):
    # Dahu plugins: bm29.subtracte.SubtractBuffer.setup
    plugin_name: Literal["bm29.subtractbuffer"]
    sample_file: str
    buffer_files: List[str]
    output_file: Optional[str] = None  # Result file name
    wait_for: Optional[List[int]] = None
    fidelity: Optional[float] = None


class HplcSummaryParameters(DahuWithIpybUploadParameters):
    # Dahu plugins: bm29.hplc.HPLC.setup
    plugin_name: Literal["bm29.hplc"]
    integrated_files: List[str]
    output_file: Optional[str] = None  # Result file name
    wait_for: Optional[List[int]] = None
    nmf_components: Optional[int] = None
