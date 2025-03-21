import uuid
from typing import Annotated

from fastapi import APIRouter, Cookie, Response
from pydantic import BaseModel

router = APIRouter(prefix="/data")

"""
TypeScript data interfaces:

export interface CourseType {
  attr_list: string;
  code_match: number;
  code_num: string;
  credit_max: number;
  credit_min: number;
  dept: string;
  desc_text: string;
  sem_list: string;
  title: string;
  title_abbrev: number;
  title_acronym: number;
  title_exact_match: number;
  title_match: number;
  title_start_match: number;
}

export type CourseEntry = {
  name: string;
  count: number;
  data: CourseType;
};

export interface SemesterType {
    semesterNumber: number;
    semesterSeason: string;
    creditsTotal: number;
    courseList: CourseType[];
}"
"""


class CourseType(BaseModel):
    attr_list: str
    code_match: int
    code_num: str
    credit_max: int
    credit_min: int
    dept: str
    desc_text: str
    sem_list: str
    title: str
    title_abbrev: int
    title_acronym: int
    title_exact_match: int
    title_match: int
    title_start_match: int


class CourseEntry(BaseModel):
    name: str
    count: int
    data: CourseType


class SemesterType(BaseModel):
    semesterNumber: int
    semesterSeason: str
    creditsTotal: int
    courseList: list[CourseType]


def generate_cookie() -> str:
    cookie_uuid = uuid.uuid4().hex
    # TODO: Store data in database
    return cookie_uuid


@router.get("/get")
def get_data(session_token: Annotated[str | None, Cookie()] = None) -> None:
    if session_token is None:
        cookie_uuid = generate_cookie()
        response = Response()
        response.set_cookie(key="session_token", value=cookie_uuid)
        return response
    # TODO: Fetch data from database


@router.get("/set")
def set_data(session_token: Annotated[str | None, Cookie()] = None) -> None:
    if session_token is None:
        cookie_uuid = generate_cookie()
        response = Response()
        response.set_cookie(key="session_token", value=cookie_uuid)
        return response
    # TODO: Store data in database
