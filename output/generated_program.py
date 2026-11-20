from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import TypeAlias


GradeBook: TypeAlias = tuple["Student", ...]


class GradeBookError(Exception):
    """성적 관리 프로그램의 기본 예외 클래스."""


class EmptyGradeBookError(GradeBookError):
    """등록된 학생이 없는 상태에서 조회 연산을 수행할 때 발생하는 예외."""


class DuplicateStudentError(GradeBookError):
    """동일한 이름의 학생을 등록할 때 발생하는 예외."""


@dataclass(frozen=True)
class Student:
    """학생의 이름과 점수를 저장하는 불변 데이터 클래스."""

    name: str
    score: float


def create_grade_book() -> GradeBook:
    """빈 성적 관리 상태를 반환한다."""
    return ()


def register_student(
    grade_book: GradeBook,
    name: str,
    score: Real,
) -> GradeBook:
    """
    학생을 등록한 새로운 성적 관리 상태를 반환한다.

    이름은 앞뒤 공백을 제거한 뒤 저장하며, 동일한 이름은 등록할 수 없다.
    기존 grade_book은 변경하지 않는다.
    """
    if not isinstance(name, str):
        raise TypeError("학생 이름은 문자열이어야 합니다.")

    normalized_name = name.strip()

    if not normalized_name:
        raise ValueError("학생 이름은 비어 있을 수 없습니다.")

    if isinstance(score, bool) or not isinstance(score, Real):
        raise TypeError("점수는 숫자여야 합니다.")

    try:
        numeric_score = float(score)
    except (OverflowError, ValueError) as exc:
        raise ValueError("점수는 유한한 숫자여야 합니다.") from exc

    if not isfinite(numeric_score):
        raise ValueError("점수는 유한한 숫자여야 합니다.")

    if not 0 <= numeric_score <= 100:
        raise ValueError("점수는 0점 이상 100점 이하이어야 합니다.")

    if any(student.name == normalized_name for student in grade_book):
        raise DuplicateStudentError(
            f"이미 등록된 학생입니다: {normalized_name}"
        )

    new_student = Student(
        name=normalized_name,
        score=numeric_score,
    )

    return (*grade_book, new_student)


def list_students(grade_book: GradeBook) -> tuple[Student, ...]:
    """
    등록된 전체 학생을 등록 순서대로 반환한다.

    학생이 없으면 빈 튜플을 반환한다.
    """
    return tuple(grade_book)


def calculate_average(grade_book: GradeBook) -> float:
    """
    전체 학생의 평균 점수를 반환한다.

    등록된 학생이 없으면 EmptyGradeBookError를 발생시킨다.
    """
    if not grade_book:
        raise EmptyGradeBookError(
            "등록된 학생이 없어 평균을 계산할 수 없습니다."
        )

    return sum(student.score for student in grade_book) / len(grade_book)


def find_top_students(
    grade_book: GradeBook,
) -> tuple[Student, ...]:
    """
    최고 점수 학생을 모두 반환한다.

    동점자는 등록 순서를 유지하여 모두 반환한다.
    등록된 학생이 없으면 EmptyGradeBookError를 발생시킨다.
    """
    if not grade_book:
        raise EmptyGradeBookError(
            "등록된 학생이 없어 최고 점수 학생을 조회할 수 없습니다."
        )

    highest_score = max(student.score for student in grade_book)

    return tuple(
        student
        for student in grade_book
        if student.score == highest_score
    )


def format_student_list(
    students: tuple[Student, ...],
) -> str:
    """학생 목록을 화면 출력용 문자열로 변환한다."""
    if not students:
        return "등록된 학생이 없습니다."

    lines = ["전체 학생 목록"]

    for index, student in enumerate(students, start=1):
        lines.append(
            f"{index}. {student.name} - {student.score:g}점"
        )

    return "\n".join(lines)


def format_average(average: float) -> str:
    """평균 점수를 화면 출력용 문자열로 변환한다."""
    return f"평균 점수: {average:g}점"


def format_top_students(
    students: tuple[Student, ...],
) -> str:
    """
    최고 점수 학생 목록을 화면 출력용 문자열로 변환한다.

    학생 목록이 비어 있으면 안내 문구를 반환한다.
    """
    if not students:
        return "최고 점수 학생이 없습니다."

    if len(students) == 1:
        student = students[0]
        return f"최고 점수 학생: {student.name} - {student.score:g}점"

    lines = ["최고 점수 학생"]

    for student in students:
        lines.append(
            f"- {student.name} - {student.score:g}점"
        )

    return "\n".join(lines)