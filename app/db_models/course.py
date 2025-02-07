from sqlalchemy.dialects.mysql import TEXT, TINYINT, VARCHAR
from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    title: str = Field(sa_type=VARCHAR(255))
    desc_text: str = Field(sa_type=TEXT)
    credit_min: int = Field(sa_type=TINYINT)
    credit_max: int = Field(sa_type=TINYINT)
