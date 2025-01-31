from sqlalchemy.dialects.mysql import ENUM, SMALLINT, TINYINT, VARCHAR
from sqlmodel import Field, SQLModel

_SEM_ENUM = [
    "Fall",
    "Spring",
    "Summer"
]

class Course_Seats(SQLModel, table=True):
    sem_year: int = Field(primary_key=True, sa_type=SMALLINT)
    semester: str = Field(primary_key=True, sa_type=ENUM(*_SEM_ENUM))
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    seats_filled: int = Field(sa_type=TINYINT)
    seats_total: int = Field(sa_type=TINYINT)