from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
import datetime
from fastapi import File, UploadFile
# 데이터의 도메인을지정해주고
# 이를 검증해준다.
from pydantic import BaseModel


class PotholeInput(BaseModel):
    file:UploadFile
    gps_x:float
    gps_y:float
    gps_z:float
    