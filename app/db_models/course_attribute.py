from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlmodel import Field, SQLModel

_ATTR_ENUM = [
    "Communication Intensive",
    "Culminating Exp/Capstone",
    "Data Intensive I",
    "Data Intensive II",
    "Writing Intensive",
    "HASS Inquiry",
    "Introductory Level Course",
    "PDII Option for Engr Majors"
]

class Course_Attribute(SQLModel, table=True):
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    attr: str = Field(primary_key=True, sa_type=ENUM(*_ATTR_ENUM))