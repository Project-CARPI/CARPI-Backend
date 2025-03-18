from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlmodel import Field, SQLModel

_CATEGORY_ENUM = ["Major", "Level", "Classification"]
_RESTRICTION_ENUM = ["Must be", "May not be"]


class Course_Restriction(SQLModel, table=True):
    dept: str = Field(primary_key=True, sa_type=VARCHAR(4))
    code_num: str = Field(primary_key=True, sa_type=VARCHAR(4))
    category: str = Field(primary_key=True, sa_type=ENUM(*_CATEGORY_ENUM))
    restr_rule: str = Field(primary_key=True, sa_type=ENUM(*_RESTRICTION_ENUM))
    restriction: str = Field(primary_key=True, sa_type=VARCHAR(255))
