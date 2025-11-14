"""
성적 관련 유틸리티 함수
"""
from typing import Optional


# 성적-평점 매핑
GRADE_TO_POINT = {
    "A+": 4.5,
    "A": 4.0,
    "A0": 4.0,  # A0는 A와 동일하게 처리
    "B+": 3.5,
    "B": 3.0,
    "B0": 3.0,  # B0는 B와 동일하게 처리
    "C+": 2.5,
    "C": 2.0,
    "C0": 2.0,  # C0는 C와 동일하게 처리
    "D+": 1.5,
    "D": 1.0,
    "D0": 1.0,  # D0는 D와 동일하게 처리
    "F": 0.0
}

# 유효한 성적 목록 (API 입력용)
VALID_GRADES = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]


def grade_to_point(grade: Optional[str]) -> float:
    """
    성적을 평점으로 변환

    Args:
        grade: 성적 (A+, A, B+, B, C+, C, D+, D, F)

    Returns:
        평점 (0.0 ~ 4.5)

    Raises:
        ValueError: 유효하지 않은 성적
    """
    if grade is None:
        return 0.0

    if grade not in GRADE_TO_POINT:
        raise ValueError(f"Invalid grade: {grade}. Valid grades: {', '.join(VALID_GRADES)}")

    return GRADE_TO_POINT[grade]


def is_valid_grade(grade: str) -> bool:
    """
    유효한 성적인지 확인

    Args:
        grade: 성적

    Returns:
        유효 여부
    """
    return grade in VALID_GRADES
