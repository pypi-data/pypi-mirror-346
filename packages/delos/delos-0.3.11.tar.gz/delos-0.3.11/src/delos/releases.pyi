from datetime import datetime
from enum import Enum
from typing import Any

from _typeshed import Incomplete
from pydantic import BaseModel

from .endpoints import DelosEndpoints as DelosEndpoints
from .endpoints import Endpoints as Endpoints

class Release(Enum):
    V1 = "v1"

class DelosClientReleases(BaseModel):
    version: Release
    release_date: datetime
    details: dict[str, Any]
    suffix: str
    available_endpoints: list[DelosEndpoints]

first_release: Incomplete
AllReleases: list[DelosClientReleases]
