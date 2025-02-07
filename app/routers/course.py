from enum import Enum

from fastapi import APIRouter
from sqlalchemy.sql import text
from sqlmodel import select

from ..db_models.course import Course
from ..db_models.course_attribute import Course_Attribute
from ..db_models.course_seats import Course_Seats
from ..dependencies import SessionDep


class CourseFilter(str, Enum):
    departments = "departments"
    attributes = "attributes"
    semesters = "semesters"


router = APIRouter(prefix="/course")


_SEARCH_COURSE_QUERY = text(
    """
    SELECT
        course.dept AS dept,
        course.code_num AS code_num,
        course.title AS title,
        course.desc_text AS desc_text,
        course.credit_min AS credit_min,
        course.credit_max AS credit_max,
        GROUP_CONCAT(DISTINCT CONCAT(course_seats.semester, ' ', course_seats.sem_year)) AS sem_list,
        GROUP_CONCAT(DISTINCT course_attribute.attr ORDER BY course_attribute.attr ASC) AS attr_list,
        REGEXP_LIKE(CONCAT(course.dept, ' ', course.code_num), :search_code_regex, 'i') AS code_match,
        REGEXP_LIKE(course.title, :search_full_regex, 'i') AS title_exact_match,
        REGEXP_LIKE(course.title, :search_start_regex, 'i') AS title_start_match,
        REGEXP_LIKE(course.title, :search_any_regex, 'i') AS title_match,
        REGEXP_LIKE(course.title, :search_acronym_regex, 'i') AS title_acronym,
        REGEXP_LIKE(course.title, :search_abbrev_regex, 'i') AS title_abbrev
    FROM
        course
        INNER JOIN course_seats USING(dept, code_num)
        LEFT JOIN course_attribute USING(dept, code_num)
    WHERE
        REGEXP_LIKE(dept, :dept_filter_regex, 'i') > 0
    GROUP BY
        dept,
        code_num,
        title,
        desc_text,
        credit_min,
        credit_max,
        code_match,
        title_exact_match,
        title_start_match,
        title_match,
        title_acronym,
        title_abbrev
    HAVING
        ( 
            code_match > 0
            OR title_exact_match > 0
            OR title_start_match > 0
            OR title_match > 0
            OR title_acronym > 0
            OR title_abbrev > 0
        )
        AND REGEXP_LIKE(IFNULL(attr_list, ''), :attr_filter_regex, 'i') > 0
        AND REGEXP_LIKE(sem_list, :sem_filter_regex, 'i') > 0
    ORDER BY
        code_match DESC,
        title_exact_match DESC,
        title_start_match DESC,
        title_match DESC,
        title_acronym DESC,
        title_abbrev DESC,
        code_num ASC,
        dept ASC
    ;
"""
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
    if not (searchPrompt or dept_filters or attr_filters or sem_filters):
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
    if searchPrompt and len(searchPrompt) > 0:
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
    params = {
        "search_code_regex": regex_code,
        "search_full_regex": regex_full,
        "search_start_regex": regex_start,
        "search_any_regex": regex_any,
        "search_acronym_regex": regex_acronym,
        "search_abbrev_regex": regex_abbrev,
        "dept_filter_regex": dept_filter_regex,
        "attr_filter_regex": attr_filter_regex,
        "sem_filter_regex": sem_filter_regex,
    }
    results = session.exec(_SEARCH_COURSE_QUERY, params=params).all()
    return [dict(row._mapping) for row in results]


@router.get("/filter/values/{filter}")
def get_filter_values(session: SessionDep, filter: CourseFilter) -> list[str]:
    column = None
    if filter is CourseFilter.departments:
        column = Course.dept
    elif filter is CourseFilter.attributes:
        column = Course_Attribute.attr
    elif filter is CourseFilter.semesters:
        column = Course_Seats.semester
    else:
        return None
    return session.exec(select(column).distinct()).all()
