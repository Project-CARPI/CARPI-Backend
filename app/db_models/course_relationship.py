from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlmodel import Field, SQLModel

_RELATIONSHIP_ENUM = ["Coreq", "Cross"]


class Course_Relationship(SQLModel, table=True):
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    relationship: str = Field(primary_key=True, sa_type=ENUM(*_RELATIONSHIP_ENUM))
    rel_dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    rel_code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
