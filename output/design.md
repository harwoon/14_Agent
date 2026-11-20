# 프로젝트 목적

학생 이름과 점수를 등록하고, 등록된 성적을 함수형 API로 관리하는 프로그램을 설계한다.

프로그램은 다음 기능을 제공한다.

- 학생 성적 등록
- 전체 학생 목록 조회
- 전체 학생 평균 점수 계산
- 최고 점수 학생 조회
- 입력 대기 없이 함수 호출만으로 동작
- Python 표준 라이브러리만 사용
- 상태를 직접 변경하지 않는 불변 데이터 구조 사용

# 필수 기능 목록

1. 학생 성적 등록
   - 이름과 점수를 전달받아 새로운 학생을 등록한다.
   - 점수는 `0점 이상 100점 이하`만 허용한다.
   - 동일한 이름의 학생은 중복 등록하지 않는다.
   - 등록 함수는 기존 상태를 변경하지 않고 새로운 상태를 반환한다.

2. 전체 학생 목록 조회
   - 등록 순서대로 모든 학생을 반환한다.
   - 등록된 학생이 없으면 빈 튜플을 반환한다.

3. 평균 점수 계산
   - 전체 학생의 평균 점수를 계산한다.
   - 등록된 학생이 없으면 예외를 발생시킨다.

4. 최고 점수 학생 조회
   - 최고 점수 학생을 반환한다.
   - 최고 점수가 같은 학생이 여러 명이면 모두 반환한다.
   - 등록된 학생이 없으면 예외를 발생시킨다.

5. 결과 문자열 변환
   - 조회 결과를 화면 출력에 사용할 수 있는 문자열로 변환한다.
   - 함수 내부에서 `input()`이나 `print()`를 호출하지 않는다.

# 자료구조

## 학생 정보

불변 `dataclass`를 사용한다.

```python
Student(
    name: str,
    score: float
)
```

## 성적 관리 상태

학생 객체를 저장하는 불변 튜플을 사용한다.

```python
GradeBook = tuple[Student, ...]
```

예시:

```python
(
    Student(name="홍길동", score=85.0),
    Student(name="김철수", score=92.0),
)
```

튜플을 사용하므로 등록 함수가 기존 데이터를 직접 수정하지 않는다.

## 정책

- 이름: 공백 제거 후 빈 문자열이면 오류
- 점수: 숫자 타입만 허용
- 점수 범위: `0 <= score <= 100`
- `bool`은 숫자로 취급하지 않음
- 동일 이름: 등록 거부
- 최고 점수 동점자: 모두 반환
- 학생이 없는 경우:
  - 목록 조회: 빈 튜플 반환
  - 평균 및 최고 점수 조회: `EmptyGradeBookError` 발생

# 함수 목록과 함수별 역할

## 예외 클래스

```python
class GradeBookError(Exception):
    """성적 관리 프로그램의 기본 예외"""
```

프로그램에서 발생하는 성적 관리 관련 예외의 기본 클래스이다.

```python
class EmptyGradeBookError(GradeBookError):
    """학생이 등록되지 않은 상태에서 조회 연산을 수행할 때 발생"""
```

평균 점수 또는 최고 점수를 조회할 학생이 없을 때 발생한다.

```python
class DuplicateStudentError(GradeBookError):
    """동일한 이름의 학생을 등록할 때 발생"""
```

이미 등록된 이름을 다시 등록할 때 발생한다.

## 데이터 클래스

```python
@dataclass(frozen=True)
class Student:
    name: str
    score: float
```

학생 이름과 점수를 저장한다. `frozen=True`를 사용하여 생성 후 값을 변경할 수 없게 한다.

## 초기 상태 생성

```python
def create_grade_book() -> GradeBook:
    ...
```

빈 성적 관리 상태를 반환한다.

## 학생 등록

```python
def register_student(
    grade_book: GradeBook,
    name: str,
    score: Real,
) -> GradeBook:
    ...
```

학생을 등록한 새로운 성적 관리 상태를 반환한다.

## 학생 목록 조회

```python
def list_students(grade_book: GradeBook) -> tuple[Student, ...]:
    ...
```

등록된 전체 학생을 등록 순서대로 반환한다.

## 평균 점수 계산

```python
def calculate_average(grade_book: GradeBook) -> float:
    ...
```

전체 학생의 평균 점수를 반환한다.

## 최고 점수 학생 조회

```python
def find_top_students(
    grade_book: GradeBook,
) -> tuple[Student, ...]:
    ...
```

최고 점수를 받은 학생을 모두 반환한다.

## 학생 목록 문자열 변환

```python
def format_student_list(
    students: tuple[Student, ...],
) -> str:
    ...
```

학생 목록을 화면 출력용 문자열로 변환한다.

## 평균 점수 문자열 변환

```python
def format_average(average: float) -> str:
    ...
```

평균 점수를 화면 출력용 문자열로 변환한다.

## 최고 점수 학생 문자열 변환

```python
def format_top_students(
    students: tuple[Student, ...],
) -> str:
    ...
```

최고 점수 학생 목록을 화면 출력용 문자열로 변환한다.

# 프로그램 흐름

1. `create_grade_book()`를 호출하여 빈 상태를 만든다.
2. `register_student()`에 이름과 점수를 전달한다.
3. 반환된 새로운 상태를 다음 연산에 사용한다.
4. `list_students()`로 전체 목록을 조회한다.
5. `calculate_average()`로 평균 점수를 계산한다.
6. `find_top_students()`로 최고 점수 학생을 조회한다.
7. 필요한 경우 `format_*()` 함수를 사용하여 결과를 문자열로 변환한다.
8. 실제 콘솔 출력은 API 외부에서 호출자가 담당한다.

예시 흐름:

```python
grade_book = create_grade_book()

grade_book = register_student(grade_book, "홍길동", 85)
grade_book = register_student(grade_book, "김철수", 92)

students = list_students(grade_book)
average = calculate_average(grade_book)
top_students = find_top_students(grade_book)

print(format_student_list(students))
print(format_average(average))
print(format_top_students(top_students))
```

# 예외 처리 요구사항

- 이름이 문자열이 아니면 `TypeError`를 발생시킨다.
- 이름이 공백뿐이면 `ValueError`를 발생시킨다.
- 점수가 숫자가 아니면 `TypeError`를 발생시킨다.
- `bool`은 점수로 허용하지 않는다.
- 점수가 `0점 미만` 또는 `100점 초과`이면 `ValueError`를 발생시킨다.
- 점수가 `NaN`, 양의 무한대, 음의 무한대이면 `ValueError`를 발생시킨다.
- 동일한 이름을 등록하면 `DuplicateStudentError`를 발생시킨다.
- 학생이 없는 상태에서 평균 점수를 계산하면 `EmptyGradeBookError`를 발생시킨다.
- 학생이 없는 상태에서 최고 점수 학생을 조회하면 `EmptyGradeBookError`를 발생시킨다.
- 학생이 없는 상태에서 목록을 조회하면 오류 대신 빈 튜플을 반환한다.
- 함수 내부에서는 `input()`으로 입력을 기다리지 않는다.
- 함수 내부에서는 `print()`를 호출하지 않는다.

# 구현 코드

```python
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import TypeAlias


GradeBook: TypeAlias = tuple["Student", ...]


class GradeBookError(Exception):
    """성적 관리 프로그램의 기본 예외 클래스."""


class EmptyGradeBookError(GradeBookError):
    """성적 관리 상태에 학생이 없을 때 발생하는 예외."""


class DuplicateStudentError(GradeBookError):
    """동일한 이름의 학생을 등록할 때 발생하는 예외."""


@dataclass(frozen=True)
class Student:
    """학생의 이름과 점수를 저장하는 불변 데이터 클래스."""

    name: str
    score: float


def create_grade_book() -> GradeBook:
    """
    빈 성적 관리 상태를 반환한다.

    Returns:
        GradeBook: 빈 학생 튜플
    """
    return ()


def register_student(
    grade_book: GradeBook,
    name: str,
    score: Real,
) -> GradeBook:
    """
    학생을 등록한 새로운 성적 관리 상태를 반환한다.

    Args:
        grade_book: 기존 성적 관리 상태
        name: 학생 이름
        score: 학생 점수

    Returns:
        GradeBook: 학생이 추가된 새로운 성적 관리 상태

    Raises:
        TypeError: 이름 또는 점수의 타입이 잘못된 경우
        ValueError: 이름이나 점수 값이 유효하지 않은 경우
        DuplicateStudentError: 동일한 이름이 이미 등록된 경우
    """
    if not isinstance(name, str):
        raise TypeError("학생 이름은 문자열이어야 합니다.")

    normalized_name = name.strip()

    if not normalized_name:
        raise ValueError("학생 이름은 비어 있을 수 없습니다.")

    if isinstance(score, bool) or not isinstance(score, Real):
        raise TypeError("점수는 숫자여야 합니다.")

    numeric_score = float(score)

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
    전체 학생 목록을 반환한다.

    Args:
        grade_book: 성적 관리 상태

    Returns:
        tuple[Student, ...]: 등록 순서대로 정렬된 학생 목록
    """
    return tuple(grade_book)


def calculate_average(grade_book: GradeBook) -> float:
    """
    전체 학생의 평균 점수를 계산한다.

    Args:
        grade_book: 성적 관리 상태

    Returns:
        float: 평균 점수

    Raises:
        EmptyGradeBookError: 등록된 학생이 없는 경우
    """
    if not grade_book:
        raise EmptyGradeBookError(
            "등록된 학생이 없어 평균을 계산할 수 없습니다."
        )

    total_score = sum(student.score for student in grade_book)
    return total_score / len(grade_book)


def find_top_students(
    grade_book: GradeBook,
) -> tuple[Student, ...]:
    """
    최고 점수 학생을 모두 반환한다.

    동점자가 있으면 등록 순서를 유지하여 모두 반환한다.

    Args:
        grade_book: 성적 관리 상태

    Returns:
        tuple[Student, ...]: 최고 점수 학생 목록

    Raises:
        EmptyGradeBookError: 등록된 학생이 없는 경우
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
    """
    학생 목록을 출력용 문자열로 변환한다.

    Args:
        students: 학생 목록

    Returns:
        str: 학생 목록 문자열
    """
    if not students:
        return "등록된 학생이 없습니다."

    lines = ["전체 학생 목록"]

    for index, student in enumerate(students, start=1):
        lines.append(
            f"{index}. {student.name} - {student.score:g}점"
        )

    return "\n".join(lines)


def format_average(average: float) -> str:
    """
    평균 점수를 출력용 문자열로 변환한다.

    Args:
        average: 평균 점수

    Returns:
        str: 평균 점수 문자열
    """
    return f"평균 점수: {average:g}점"


def format_top_students(
    students: tuple[Student, ...],
) -> str:
    """
    최고 점수 학생 목록을 출력용 문자열로 변환한다.

    Args:
        students: 최고 점수 학생 목록

    Returns:
        str: 최고 점수 학생 문자열
    """
    if not students:
        return "최고 점수 학생이 없습니다."

    if len(students) == 1:
        student = students[0]
        return (
            f"최고 점수 학생: "
            f"{student.name} - {student.score:g}점"
        )

    lines = ["최고 점수 학생"]

    for student in students:
        lines.append(
            f"- {student.name} - {student.score:g}점"
        )

    return "\n".join(lines)
```

## 사용 예시

```python
grade_book = create_grade_book()

grade_book = register_student(grade_book, "홍길동", 85)
grade_book = register_student(grade_book, "김철수", 92)
grade_book = register_student(grade_book, "이영희", 92)

students = list_students(grade_book)
average = calculate_average(grade_book)
top_students = find_top_students(grade_book)

print(format_student_list(students))
print()
print(format_average(average))
print()
print(format_top_students(top_students))
```

실행 결과:

```text
전체 학생 목록
1. 홍길동 - 85점
2. 김철수 - 92점
3. 이영희 - 92점

평균 점수: 89.66666666666667점

최고 점수 학생
- 김철수 - 92점
- 이영희 - 92점
```