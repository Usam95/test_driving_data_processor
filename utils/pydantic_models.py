import json
import glob
import os

import pydantic
from pydantic import BaseModel
from pydantic import ValidationError
from typing import Optional, List, Dict


# Pydantic models
class TestDrivingData(BaseModel):
    group_vehicle_number: str
    record_country: str
    record_date: str
    comment: Optional[str] = None
    total_driven_km: str


class Config(BaseModel):
    dataset_path: str
    output_data_path: str
    clean_data: bool
    default_total_driven_km: str
    default_group_vehicle_number: str
    default_record_country: str
    default_record_date: str

    logging_level: str
