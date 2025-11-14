from enum import Enum

from carpi_data_model.models import (
    Attribute,
    Course,
    Course_Attribute,
    Course_Offering,
    Subject,
)
from fastapi import APIRouter
from sqlalchemy import and_, desc, distinct, func, or_, select
from sqlalchemy.sql import Select

from app import SessionDep


class CourseFilter(str, Enum):
    subjects = "subjects"
    attributes = "attributes"
    semesters = "semesters"


router = APIRouter(prefix="/course")


def search_course_query(
    search_code_regex: str,
    search_full_regex: str,
    search_start_regex: str,
    search_any_regex: str,
    search_acronym_regex: str,
    search_abbrev_regex: str,
    dept_filter_regex: str,
    attr_filter_regex: str,
    sem_filter_regex: str,
) -> Select:
    return (
        select(
            Course.subj_code,
            Course.code_num,
            Course.title,
            Course.desc_text,
            Course.credit_min,
            Course.credit_max,
            func.group_concat(distinct(Course_Offering.semester)).label("sem_list"),
            func.group_concat(distinct(Course_Attribute.attr_code)).label("attr_list"),
            func.regexp_like(
                func.concat(Course.subj_code, " ", Course.code_num),
                search_code_regex,
                "i",
            ).label("code_match"),
            func.regexp_like(Course.title, search_full_regex, "i").label(
                "title_exact_match"
            ),
            func.regexp_like(Course.title, search_start_regex, "i").label(
                "title_start_match"
            ),
            func.regexp_like(Course.title, search_any_regex, "i").label("title_match"),
            func.regexp_like(Course.title, search_acronym_regex, "i").label(
                "title_acronym"
            ),
            func.regexp_like(Course.title, search_abbrev_regex, "i").label(
                "title_abbrev"
            ),
        )
        .join(
            Course_Offering,
            and_(
                Course.subj_code == Course_Offering.subj_code,
                Course.code_num == Course_Offering.code_num,
            ),
        )
        .outerjoin(
            Course_Attribute,
            and_(
                Course.subj_code == Course_Attribute.subj_code,
                Course.code_num == Course_Attribute.code_num,
            ),
        )
        .where(func.regexp_like(Course.subj_code, dept_filter_regex, "i"))
        .group_by(
            Course.subj_code,
            Course.code_num,
            Course.title,
            Course.desc_text,
            Course.credit_min,
            Course.credit_max,
        )
        .having(
            or_(
                func.regexp_like(
                    func.concat(Course.subj_code, " ", Course.code_num),
                    search_code_regex,
                    "i",
                ),
                func.regexp_like(Course.title, search_full_regex, "i"),
                func.regexp_like(Course.title, search_start_regex, "i"),
                func.regexp_like(Course.title, search_any_regex, "i"),
                func.regexp_like(Course.title, search_acronym_regex, "i"),
                func.regexp_like(Course.title, search_abbrev_regex, "i"),
            ),
            func.regexp_like(
                func.ifnull(
                    func.group_concat(distinct(Course_Attribute.attr_code)), ""
                ),
                attr_filter_regex,
                "i",
            ),
            func.regexp_like(
                func.group_concat(
                    distinct(
                        func.concat(
                            Course_Offering.semester, " ", Course_Offering.sem_year
                        )
                    )
                ),
                sem_filter_regex,
                "i",
            ),
        )
        .order_by(
            desc(
                func.regexp_like(
                    func.concat(Course.subj_code, " ", Course.code_num),
                    search_code_regex,
                    "i",
                )
            ),
            desc(func.regexp_like(Course.title, search_full_regex, "i")),
            desc(func.regexp_like(Course.title, search_start_regex, "i")),
            desc(func.regexp_like(Course.title, search_any_regex, "i")),
            desc(func.regexp_like(Course.title, search_acronym_regex, "i")),
            desc(func.regexp_like(Course.title, search_abbrev_regex, "i")),
            Course.code_num,
            Course.subj_code,
        )
    )


@router.get("/search")
def search_course(
    session: SessionDep,
    searchPrompt: str | None = None,
    deptFilters: str | None = None,
    attrFilters: str | None = None,
    semFilters: str | None = None,
) -> list[dict[str, str | int | None]]:
    # FastAPI does not support list query parameters
    dept_filters = deptFilters.split(",") if deptFilters else None
    attr_filters = attrFilters.split(",") if attrFilters else None
    sem_filters = semFilters.split(",") if semFilters else None
    if not (dept_filters or attr_filters or sem_filters):
        if not searchPrompt or len(searchPrompt) < 3:
            return []
    regex_code = ".*"
    regex_full = ".*"
    regex_start = ".*"
    regex_any = ".*"
    regex_acronym = ".*"
    regex_abbrev = ".*"
    dept_filter_regex = ".*"
    attr_filter_regex = ".*"
    sem_filter_regex = ".*"
    if dept_filters and len(dept_filters) > 0:
        dept_filters.sort()
        dept_filter_regex = "|".join(dept_filters)
    if attr_filters and len(attr_filters) > 0:
        attr_filters.sort()
        attr_filter_regex = ".*".join(attr_filters)
    if sem_filters and len(sem_filters) > 0:
        sem_filters.sort()
        sem_filter_regex = ".*".join(sem_filters)
    if searchPrompt and len(searchPrompt) > 2:
        reg_start_or_space = "(^|.* )"
        # Full code match
        regex_code = f"^{searchPrompt}$"
        # Full title match
        regex_full = f"^{searchPrompt}$"
        # Title match at beginning
        regex_start = f"^{searchPrompt}"
        # Title match anywhere
        regex_any = searchPrompt
        # Acronyms
        regex_acronym = reg_start_or_space
        for char in searchPrompt:
            # Don't use spaces in acronyms
            if char != " ":
                regex_acronym += f"{char}.* "
        regex_acronym = regex_acronym[:-3]
        # Abbreviations
        regex_abbrev = ""
        tokens = searchPrompt.split()
        if len(tokens) > 1:
            regex_abbrev += reg_start_or_space
            for token in tokens:
                regex_abbrev += f"{token}.* "
            regex_abbrev = regex_abbrev[:-3]
        else:
            regex_abbrev = "a^"
    results = session.execute(
        search_course_query(
            regex_code,
            regex_full,
            regex_start,
            regex_any,
            regex_acronym,
            regex_abbrev,
            dept_filter_regex,
            attr_filter_regex,
            sem_filter_regex,
        )
    ).all()
    return [dict(row._mapping) for row in results]


@router.get("/filter/values/{filter}")
def get_filter_values(session: SessionDep, filter: CourseFilter) -> list[str]:
    column = None
    if filter is CourseFilter.subjects:
        column = Subject.subj_code
    elif filter is CourseFilter.attributes:
        column = Attribute.attr_code
    elif filter is CourseFilter.semesters:
        column = Course_Offering.semester
    else:
        return None
    return session.execute(select(column).distinct()).scalars().all()
