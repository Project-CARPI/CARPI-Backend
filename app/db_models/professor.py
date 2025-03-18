from sqlalchemy.dialects.mysql import ENUM, VARCHAR, SMALLINT
from sqlmodel import Field, SQLModel

_SEMESTER_ENUM = ["Fall", "Spring", "Summer"]


class Professor(SQLModel, table=True):
    sem_year: int = Field(primary_key=True, sa_type=SMALLINT)
    semester: str = Field(primary_key=True, sa_type=ENUM(*_SEMESTER_ENUM))
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    prof_name: str = Field(primary_key=True, sa_type=VARCHAR(255))
