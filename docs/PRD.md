# MagicSquare_1004 — PRD (Product Requirements Document)

**버전:** 0.1 (초안)  
**작성일:** 2026-06-04  
**상태:** 세션 3 — 문제 정의  
**근거:** Mom Test 문제 정의 (`Report/01.MagicSquare_ProblemDefinition_Report.md`)

---

## 1. 개요

### 1.1 한 줄 요약

4×4 부분 마방진(빈칸 2, 합 34) 학습자가 풀이 후 **행·열·대각선 10개 조건**을 빠짐없이 검증할 수 있는 **CLI 검증 도구**를 만든다.

### 1.2 배경 (Mom Test)

| 항목 | 내용 |
|------|------|
| 페르소나 | 4×4 격자, 빈칸 2개(0), 1~16, 합 34 맞추는 학습자 |
| 진짜 문제 | 행·열은 맞췄으나 **대각선 검증 누락** → 틀린 상태를 늦게 발견 → **약 20분 추가 소요** |
| 증거 | (1) 확인 시간 과다 (2) 설명 어려움 (3) 늦은 발견 후 그날 포기 |

### 1.3 이번 버전에서 하지 않음

- 자동 풀이, 힌트, 튜토리얼
- n×n 일반화, 문제 생성, 게임화
- GUI, 공유·저장, SNS

---

## 2. 목표 및 성공 기준

### 2.1 제품 목표

학습자가 채운 4×4 격자에 대해 **모든 마방진 조건**을 한 번에 점검하고, **어느 조건이 실패했는지** 즉시 파악한다.

### 2.2 성공 기준

| ID | 기준 | Mom Test 연결 | 검증 방법 |
|----|------|---------------|-----------|
| S1 | 10개 조건(행4+열4+대각2) **일괄 점검** | 확인 시간 과다 | 단일 Command 1회 실행 |
| S2 | 실패 시 **조건명 + 실제합 + 기대합** 출력 | 설명 어려움 | 출력 포맷 테스트 |
| S3 | 행·열 OK + 대각선 NG → **즉시 실패** | 20분 낭비 재현 방지 | 회귀 테스트 케이스 |

---

## 3. 사용자 및 시나리오

### 3.1 Primary User

4×4 부분 마방진을 **손으로 풀거나 코드로 다루는 학습자**

### 3.2 핵심 시나리오

1. 학습자가 빈칸 2개를 채운 4×4 격자를 준비한다.
2. `verify` Command로 격자를 입력한다.
3. 10개 조건 각각 pass/fail을 확인한다.
4. fail이 있으면 **어느 행·열·대각선**인지 보고 수정한다.
5. 전부 pass면 풀이 완료로 판단한다.

### 3.3 대표 실패 시나리오 (Must Fix)

- 행·열 합은 모두 34이나 **주대각선 또는 부대각선** 합이 34가 아님  
  → 즉시 NG, 해당 대각선 명시

---

## 4. R-G-I-O

| | 요구사항 |
|---|----------|
| **Role** | 학습자 (풀이 후 self-check) |
| **Goal** | 10개 조건 전수 검증 + 실패 위치 식별 |
| **Input** | 4×4 정수 배열. 값域: `0`(빈칸) 또는 `1~16`. 1~16은 각 최대 1회. `0`은 최대 2개 |
| **Output** | 전체 OK/NG, 조건별 상세 (이름, pass/fail, sum, expected=34) |

---

## 5. 기능 요구사항

### 5.1 Rule (도메인 규칙)

**FR-R1.** 4×4 격자만 지원  
**FR-R2.** Magic constant = **34**  
**FR-R3.** 사용 숫자: **1~16**, 각 숫자 최대 1회  
**FR-R4.** 빈칸: **`0`**, 최대 **2개**  
**FR-R5.** 검증 대상 **10개**:
- Row 0, Row 1, Row 2, Row 3
- Col 0, Col 1, Col 2, Col 3
- Main diagonal (↘)
- Anti diagonal (↙)

**FR-R6.** `0`이 포함된 줄/대각선은 합 검증 시 **skip** 또는 **incomplete**로 표시 (구현 시 Test Loop에서 확정)

### 5.2 Command

**FR-C1.** CLI entry: `verify` (또는 `python -m magic1004 verify`)  
**FR-C2.** 입력 형식: 파일 경로 또는 stdin (4×4, 공백/쉼표 구분)  
**FR-C3.** 출력:
- `OK` — 10개 조건 모두 pass (빈칸 없는 완성판 기준)
- `FAIL` — 1개 이상 fail, 각 fail 항목 한 줄씩  
  예: `FAIL anti_diagonal sum=32 expected=34`

**FR-C4.** Exit code: 0 = OK, 1 = FAIL, 2 = 입력 오류

### 5.3 Skill (선택)

**FR-S1.** Rule + Command 로직을 **재사용 가능 모듈/함수**로 분리  
**FR-S2.** 외부에서 `verify_grid(grid: list[list[int]]) -> VerifyResult` 형태로 호출 가능

### 5.4 Test Loop

**FR-T1.** TDD: 실패 테스트 → 구현 → 리팩터  
**FR-T2.** 필수 테스트 케이스:
| 케이스 | 기대 |
|--------|------|
| 완성 마방진 (빈칸 없음) | OK |
| 행·열 OK, 주대각 NG | FAIL + main_diagonal 명시 |
| 1~16 중복 | FAIL (invalid grid) |
| `0` 3개 이상 | FAIL (invalid grid) |
| 빈칸 2개 남은 중간판 | incomplete/skip 정책에 따름 |

---

## 6. 비기능 요구사항

| ID | 요구 |
|----|------|
| NFR-1 | Python 3.10+ (또는 프로젝트 표준 확정 후 갱신) |
| NFR-2 | 외부 의존성 최소 (stdlib 우선) |
| NFR-3 | 단일 격자 검증 < 1초 |
| NFR-4 | README에 사용 예 1개 |

---

## 7. 8계층 로드맵 (세션 3 스코프)

```
[세션 3]  Rule → Command → (Skill) → Test Loop
[이후]    UI → Workflow → Agent → Product
```

| 계층 | v0.1 | 비고 |
|------|------|------|
| Rule | ✅ | 도메인 상수·검증 목록 |
| Command | ✅ | CLI verify |
| Skill | ✅ | verify_grid API |
| Test Loop | ✅ | pytest 등 |
| UI | — | 세션 4+ |
| Workflow | — | — |
| Agent | — | — |
| Product | — | — |

---

## 8. 마일스톤

| 단계 | 산출물 | Done 조건 |
|------|--------|-----------|
| M1 | Rule + 테스트 스켈레ton | 10개 조건 이름·expected sum 정의 |
| M2 | verify Command MVP | S1 충족 |
| M3 | fail 메시지 상세화 | S2 충족 |
| M4 | 대각선 NG 회귀 테스트 | S3 충족 |

---

## 9. 리스크 및 가정

| 리스크 | 대응 |
|--------|------|
| 빈칸 있는 중간판 검증 정책 모호 | Test Loop에서 `incomplete` vs `fail` 명시적 결정 |
| 범위 creep (자동 풀이 등) | PRD Out of Scope 고정 |
| Mom Test 표본 1명 | v0.1은 본인 학습자 페르소나 검증용 |

**가정:** 학습자는 4×4 마방진 규칙(합 34)을 이미 알고 있다.

---

## 10. 참고 문서

- `Report/01.MagicSquare_ProblemDefinition_Report.md`
- `Report/01.Mom-Test-STEP1-Report.md`
- `Prompting/01.Mom-Test-STEP1-Transcript.md`
