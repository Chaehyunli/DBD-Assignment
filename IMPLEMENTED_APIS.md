# 구현된 API 목록

**프로젝트**: DBD Assignment API
**작성일**: 2025-11-14
**총 API 수**: 8개

---

## 목차

1. [Course API (1개)](#1-course-api)
2. [Lecture API (4개)](#2-lecture-api)
3. [Scholarship API (1개)](#3-scholarship-api)
4. [Student API (2개)](#4-student-api)
5. [API 요약](#5-api-요약)

---

## 1. Course API

### 1.1 특정 과목을 담당하는 교수 조회

**GET** `/api/v1/courses/{course_code}/professors`

**설명**: (UR010) 특정 과목을 담당했던 (혹은 담당하는) 모든 교수의 목록을 조회합니다.

**Path Parameters**:
- `course_code` (string): 과목 코드 (예: CS101)

**Response (200 OK)**:
```json
[
  {
    "professor_id": "P0001",
    "professor_name": "김철수",
    "email": "kim@univ.ac.kr",
    "office_room": null
  }
]
```

**Error**:
- `404 Not Found`: Course not found

**테이블**: course → lecture → professor (3-way join)

---

## 2. Lecture API

### 2.1 강의 개설

**POST** `/api/v1/lectures`

**설명**: (UR005) 새로운 강의(Lecture)를 개설합니다.

**Request Body**:
```json
{
  "semester": "2025-1",
  "lecture_time": "월 10:00-12:00",
  "lecture_room": "공학관 301호",
  "capacity": 100,
  "course_code": "CS101",
  "professor_id": "P0001"
}
```

**Response (201 Created)**:
```json
{
  "lecture_id": 18,
  "semester": "2025-1",
  "lecture_time": "월 10:00-12:00",
  "lecture_room": "공학관 301호",
  "capacity": 100,
  "course_code": "CS101",
  "professor_id": "P0001"
}
```

**테이블**: lecture

---

### 2.2 특정 강의 상세 조회

**GET** `/api/v1/lectures/{lecture_id}`

**설명**: (8) 고유한 lecture_id로 특정 강의 하나의 상세 정보를 조회합니다.

**Path Parameters**:
- `lecture_id` (integer): 강의 ID

**Response (200 OK)**:
```json
{
  "lecture_id": 1,
  "semester": "2025-1",
  "lecture_time": "월 10:00-12:00",
  "lecture_room": "공학관 301호",
  "capacity": 100,
  "course_code": "CS101",
  "professor_id": "P0001"
}
```

**Error**:
- `404 Not Found`: Lecture not found

**테이블**: lecture

---

### 2.3 강의 목록 조회 (필터링)

**GET** `/api/v1/lectures`

**설명**: (7, 9, 10 통합) 강의 목록을 조회합니다. 과목코드, 학기, 교수번호를 쿼리 파라미터로 제공하여 결과를 필터링할 수 있습니다.

**Query Parameters** (모두 optional):
- `semester` (string): 특정 학기로 필터링 (예: "2025-2")
- `course_code` (string): 특정 과목 코드로 필터링 (예: "BUS101")
- `professor_id` (string): 특정 교수 번호로 필터링 (예: "P4001")

**Response (200 OK)**:
```json
[
  {
    "lecture_id": 1,
    "semester": "2025-1",
    "lecture_time": "월 10:00-12:00",
    "lecture_room": "공학관 301호",
    "capacity": 100,
    "course_code": "CS101",
    "professor_id": "P0001"
  }
]
```

**사용 예시**:
- 모든 강의: `GET /api/v1/lectures`
- 2025-1학기 강의: `GET /api/v1/lectures?semester=2025-1`
- CS101 과목 강의: `GET /api/v1/lectures?course_code=CS101`
- P0001 교수 강의: `GET /api/v1/lectures?professor_id=P0001`

**테이블**: lecture

---

### 2.4 특정 강의 수강생 목록 조회

**GET** `/api/v1/lectures/{lecture_id}/students`

**설명**: (UR009) 특정 강의(lecture)를 수강하는 모든 학생 명단을 조회합니다.

**Path Parameters**:
- `lecture_id` (integer): 강의 ID

**Response (200 OK)**:
```json
[
  {
    "student_id": "S1000001",
    "student_name": "이민준",
    "department_name": "컴퓨터공학과",
    "grade_year": 3,
    "grade_received": "A+"
  }
]
```

**Error**:
- `404 Not Found`: Lecture not found

**테이블**: enrollment → student → department (3-way join)

---

## 3. Scholarship API

### 3.1 장학금 대상자 선별

**GET** `/api/v1/scholarship/candidates`

**설명**: (UR012) 특정 학기의 평점 기준을 충족하는 재학생 명단을 조회합니다.

**Query Parameters**:
- `semester` (string, required): 학기 (예: "2025-2")
- `gpa_threshold` (float, required): 최소 GPA 기준 (0.0 ~ 4.5)
- `status` (string, optional): 재학 상태 (기본값: "재학")

**Response (200 OK)**:
```json
[
  {
    "student_id": "S1000008",
    "student_name": "정시우",
    "department_name": "기계공학과",
    "status": "재학",
    "semester": "2025-1",
    "semester_gpa": 4.31
  }
]
```

**Error**:
- `400 Bad Request`: 필수 파라미터 누락 또는 잘못된 값
- `422 Validation Error`: 유효성 검증 실패

**사용 예시**:
```
GET /api/v1/scholarship/candidates?semester=2025-1&gpa_threshold=4.0&status=재학
```

**테이블**: student_semester_gpa → student → department (3-way join)

---

## 4. Student API

### 4.1 학생 성적 수정 (평점 연쇄 업데이트)

**PATCH** `/api/v1/students/{student_id}/lectures/{lecture_id}/grade`

**설명**: (UR008) 특정 학생의 수강 성적을 수정하고, 연관된 학기 평점 및 전체 평점을 갱신합니다.

**Path Parameters**:
- `student_id` (string): 학번 (예: "S1000001")
- `lecture_id` (integer): 강의 ID (예: 1)

**Request Body**:
```json
{
  "grade": "B+"
}
```

**Response (200 OK)**:
```json
{
  "student_id": "S1000001",
  "lecture_id": 1,
  "updated_grade": "B+",
  "message": "성적이 성공적으로 수정되었으며, 평점이 연쇄 갱신되었습니다.",
  "updated_semester_gpa": 3.67,
  "updated_overall_gpa": 3.58
}
```

**Error**:
- `404 Not Found`: 학생 또는 수강 내역이 존재하지 않음
- `422 Validation Error`: 잘못된 성적 입력

**트랜잭션 처리**:
1. enrollment.grade 수정
2. student_semester_gpa 재계산 및 업데이트
3. student.overall_gpa 재계산 및 업데이트

**유효한 성적**: A+, A, B+, B, C+, C, D+, D, F

**테이블**: enrollment, student_semester_gpa, student, lecture, course

---

### 4.2 학생 성적표 조회

**GET** `/api/v1/students/{student_id}/report`

**설명**: (UR007) 특정 학생의 전체 성적표를 학기별로 조회합니다.

**Path Parameters**:
- `student_id` (string): 학번 (예: "S1000001")

**Response (200 OK)**:
```json
{
  "student_id": "S1000001",
  "student_name": "이민준",
  "department_name": "컴퓨터공학과",
  "overall_gpa": 3.75,
  "semesters": [
    {
      "semester": "2025-1",
      "semester_gpa": 4.0,
      "earned_credits": 9,
      "courses": [
        {"course_name": "자료구조", "credits": 3, "grade": "A0"},
        {"course_name": "프로그래밍기초", "credits": 3, "grade": "A+"},
        {"course_name": "회로이론", "credits": 3, "grade": "B+"}
      ]
    },
    {
      "semester": "2025-2",
      "semester_gpa": 3.5,
      "earned_credits": 9,
      "courses": [
        {"course_name": "자료구조", "credits": 3, "grade": "B+"},
        {"course_name": "프로그래밍기초", "credits": 3, "grade": "A0"},
        {"course_name": "회로이론", "credits": 3, "grade": "B0"}
      ]
    }
  ]
}
```

**Error**:
- `404 Not Found`: 학생이 존재하지 않음

**테이블**: student → department, student_semester_gpa, enrollment → lecture → course (5-way join)

---

## 5. API 요약

### 5.1 도메인별 API 수

| 도메인 | API 수 | 엔드포인트 |
|--------|--------|-----------|
| **Course** | 1 | `/api/v1/courses/*` |
| **Lecture** | 4 | `/api/v1/lectures/*` |
| **Scholarship** | 1 | `/api/v1/scholarship/*` |
| **Student** | 2 | `/api/v1/students/*` |
| **총계** | **8** | - |

### 5.2 HTTP Method별 분류

| Method | 개수 | 용도 |
|--------|------|------|
| **GET** | 6 | 조회 |
| **POST** | 1 | 생성 |
| **PATCH** | 1 | 수정 |
| **총계** | **8** | - |

### 5.3 주요 기능

#### 조회 기능 (6개)
1. ✅ 과목별 교수 조회
2. ✅ 강의 상세 조회
3. ✅ 강의 목록 조회 (필터링)
4. ✅ 강의별 수강생 조회
5. ✅ 장학금 대상자 조회
6. ✅ 학생 성적표 조회

#### 생성 기능 (1개)
7. ✅ 강의 개설

#### 수정 기능 (1개)
8. ✅ 성적 수정 (평점 연쇄 업데이트)

### 5.4 복잡한 쿼리

#### 3-way Join (3개)
- Course API: course → lecture → professor
- Lecture API (수강생): enrollment → student → department
- Scholarship API: student_semester_gpa → student → department

#### 5-way Join (1개)
- Student API (성적표): student → department, student_semester_gpa, enrollment → lecture → course

#### 트랜잭션 (1개)
- Student API (성적 수정): 3개 테이블 동시 업데이트 (enrollment, student_semester_gpa, student)

### 5.5 데이터베이스 현황

| 테이블 | 레코드 수 |
|--------|-----------|
| course | 11개 |
| professor | 8개 |
| lecture | 17개 |
| student | 13개 |
| enrollment | 66개 |
| student_semester_gpa | 23개 |
| department | 7개 |

---

## 6. API 테스트 방법

### 6.1 서버 실행
```bash
uvicorn app.main:app --reload
```

### 6.2 API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6.3 예시 요청

#### Course API
```bash
curl -X GET "http://localhost:8000/api/v1/courses/CS101/professors"
```

#### Lecture API
```bash
# 강의 목록
curl -X GET "http://localhost:8000/api/v1/lectures?semester=2025-1"

# 강의 개설
curl -X POST "http://localhost:8000/api/v1/lectures" \
  -H "Content-Type: application/json" \
  -d '{
    "semester": "2025-1",
    "capacity": 100,
    "course_code": "CS101",
    "professor_id": "P0001"
  }'
```

#### Scholarship API
```bash
curl -X GET "http://localhost:8000/api/v1/scholarship/candidates?semester=2025-1&gpa_threshold=4.0&status=재학"
```

#### Student API
```bash
# 성적 수정
curl -X PATCH "http://localhost:8000/api/v1/students/S1000001/lectures/1/grade" \
  -H "Content-Type: application/json" \
  -d '{"grade": "A+"}'

# 성적표 조회
curl -X GET "http://localhost:8000/api/v1/students/S1000001/report"
```

---

## 7. 프로젝트 구조

```
app/
├── main.py                         # FastAPI 앱 진입점
├── src/
│   ├── core/
│   │   ├── config.py              # 설정
│   │   └── grade_utils.py         # 성적 변환 유틸리티
│   ├── db/
│   │   └── base.py                # DB 연결
│   └── domain/
│       ├── course/                # Course 도메인 (1 API)
│       ├── lecture/               # Lecture 도메인 (4 API)
│       ├── scholarship/           # Scholarship 도메인 (1 API)
│       ├── student/               # Student 도메인 (2 API)
│       ├── professor/             # Professor 모델
│       ├── department/            # Department 모델
│       ├── enrollment/            # Enrollment 모델
│       └── student_semester_gpa/  # StudentSemesterGPA 모델
└── templates/                     # Jinja2 템플릿
```

각 도메인 폴더 구조:
```
domain/[name]/
├── __init__.py
├── model.py          # SQLAlchemy 모델
├── schema.py         # Pydantic 스키마
├── repository.py     # 데이터베이스 쿼리
├── service.py        # 비즈니스 로직
└── controller.py     # API 엔드포인트
```

---

## 8. 구현 완료 확인

| 기능 | 상태 | 비고 |
|------|------|------|
| Course API | ✅ | 1개 엔드포인트 |
| Lecture API | ✅ | 4개 엔드포인트 |
| Scholarship API | ✅ | 1개 엔드포인트 |
| Student API | ✅ | 2개 엔드포인트 |
| 모델-DB 일치성 | ✅ | 100% 일치 |
| API 테스트 | ✅ | 모두 통과 |
| 트랜잭션 처리 | ✅ | 성적 수정 API |
| 에러 처리 | ✅ | 404, 400, 422, 500 |

---

**문서 끝**
