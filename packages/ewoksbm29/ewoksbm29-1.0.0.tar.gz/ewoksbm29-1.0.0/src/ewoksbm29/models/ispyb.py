import datetime
import os
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import field_validator


class ISPyBMetadata(BaseModel):
    experiment_id: Optional[int] = None
    run_number: Union[int, List[int], None] = None
    proposal_name: Optional[str] = None
    proposal_session_name: Optional[str] = None
    beamline: Optional[str] = None
    sample_name: Optional[str] = None
    archive_root_directory: str = "/data/pyarch"

    @property
    def ispyb_parameters(self) -> dict:
        return {
            "experiment_id": self.experiment_id,
            "run_number": self.run_number,
            "pyarch": self.archive_directory,
        }

    @field_validator("proposal_session_name")
    @classmethod
    def check_date(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return
        try:
            datetime.datetime.strptime(value, "%Y%m%d")
        except ValueError:
            raise ValueError("proposal_session_name must be in YYYYmmdd format")
        return value

    @field_validator("proposal_name", "beamline")
    @classmethod
    def lower(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return
        return value.lower()

    @property
    def archive_directory(self) -> Optional[str]:
        args = (
            self.archive_root_directory,
            self.year,
            self.beamline,
            self.proposal_name,
            self.proposal_session_name,
            self.sample_name,
        )
        if any(p is None for p in args):
            return
        return os.path.join(*args)

    @property
    def year(self) -> Optional[str]:
        if self.proposal_session_name is None:
            return
        return self.proposal_session_name[:4]
