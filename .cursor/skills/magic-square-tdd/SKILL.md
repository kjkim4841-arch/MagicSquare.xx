---
name: magic-square-tdd
description: MagicSquare_1004 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차
---

# MagicSquare_xx — Dual-Track TDD · ECB

헌법: `.cursorrules`, `docs/PRD.md`. 테스트 ID 목록: [reference.md](reference.md).

---

## 언제 이 Skill을 켜는지

다음 **하나라도** 해당하면 본 Skill을 적용한다.

- `src/entity`, `src/control`, `src/boundary` 또는 `tests/**`에 **구현·테스트**를 추가·수정할 때
- 사용자가 **TDD**, **RED/GREEN/REFACTOR**, **D-***, **U-***, **ECB**, **Dual-Track**을 언급할 때
- `verify`, `MagicConstant`, **E001~E007**, **10조건 검증**, **`int[6]`** 솔루션을 다룰 때
- PRD **FR-T2** 필수 케이스·회귀 테스트를 작성할 때

**끄는 조건:** 문서만 편집, Report/Prompting만 작성, git commit/push만 요청(구현 없음).

시작 시 **한 줄 선언** (한국어 응답):

`Phase=RED | Layer=entity | Track=Logic(D-DOMAIN-*)`

---

## Logic Track vs UI Track

| Track | Layer | 테스트 ID | 파일 | pytest marker | Mock |
|-------|-------|-----------|------|---------------|------|
| **Logic** | entity, control | `D-*` | `tests/{entity,control}/test_d_*.py` | `entity` / `control` | **Domain Mock 금지** (`patch`·가짜 entity 금지) |
| **UI** | boundary | `U-*` | `tests/boundary/test_u_*.py` | `boundary` | **I/O·CLI Mock 허용** |

- `test_d_*` → Logic, `test_u_*` → UI. 혼용 금지.
- FR-T2 필수 케이스 ID는 [reference.md](reference.md)의 `D-*`와 매핑.

---

## ECB · Mock · E001~E007

**의존 (단방향):**

```
boundary ──► control ──► entity
```

| 규칙 | 내용 |
|------|------|
| boundary | CLI, stdin/파일, **E001~E007** 발생·반환, exit code (PRD FR-C4) |
| control | 유스케이스 조율, entity만 호출, **boundary import 금지** |
| entity | 격자·합 34·검증/솔루션 순수 로직, **E001~E005 처리·발생 금지**, **상위/형제 import 금지** |
| boundary | **entity 직접 호출 금지** — control만 |

**출력 계약 (혼용 금지):**

- **검증 CLI** (boundary): PRD FR-C3 — `OK` / `FAIL … expected=34`
- **솔버 성공** (control→entity): `int[6]` `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index**

**Mock:**

- Logic: 실제 grid·MagicConstant SSOT만 사용.
- UI: subprocess, stdin, 임시 파일 Mock 가능. **Golden/snapshot 갱신은 사용자 명시 승인 없이 금지.**

**용어:** FR-R6 도메인 `skip`/`incomplete` ≠ `pytest.skip()` — 테스트 회피용 skip·xfail만 금지.

---

## RED (5~7단계)

1. **선언:** Phase=RED, Layer, Track, 대상 `D-*` 또는 `U-*` ID.
2. **범위:** 한 행동만 — 한 테스트 함수 또는 한 실패 이유.
3. **위치:** `tests/{entity|control|boundary}/test_d_*` 또는 `test_u_*`.
4. **작성:** 실패하는 assert 1개 이상; MagicConstant는 SSOT import(리터럴 `34`/`16`/`4` 금지).
5. **실행:** 해당 파일 또는 `-m entity|control|boundary` — **실패 확인 필수**.
6. **금지:** 구현 선행, assert 완화, `skip`/`xfail`, GREEN으로 Phase 넘김.
7. **기록:** 실패 메시지·테스트 ID를 완료 보고에 남김.

---

## GREEN (5~7단계)

1. **선언:** Phase=GREEN, 동일 Layer·Track·테스트 ID.
2. **최소 구현:** RED를 통과하는 최소 코드만 (`src/` 해당 Layer).
3. **ECB:** entity에 I/O·E00x 없음; boundary에 도메인 규칙 없음.
4. **SSOT:** 상수는 `MagicConstant`(entity) 한 곳에서만 추가.
5. **실행:** RED에서 돌린 **동일 pytest** — **통과 확인**.
6. **금지:** 다른 Layer 선행 확장, 테스트 삭제, assert 약화.
7. **기록:** 변경 파일·공개 API 한 줄.

---

## REFACTOR (5~7단계)

1. **선언:** Phase=REFACTOR, Layer·Track 유지.
2. **전제:** 해당 Track 관련 테스트 **이미 green**.
3. **리팩터:** 이름·중복 제거·구조만; **행위 변경 없음**.
4. **실행:** Layer marker → Track 전체 → **전체 `pytest`** 순 (아래 Test/Review Loop).
5. **금지:** RED 테스트 제거, 새 기능 추가(새 RED로 분리).
6. **회귀:** FR-T2 `D-*` 전부 green인지 확인.
7. **기록:** 리팩터 요약·다음 RED 후보 ID.

---

## Test / Review Loop — pytest 언제 돌리는지

| 시점 | 명령 | 목적 |
|------|------|------|
| RED 직후 | `pytest path/to/test_d_xxx.py -q` | 의도적 **실패** 확인 |
| GREEN 직후 | **동일 path** `-q` | 해당 테스트 **통과** |
| REFACTOR 중 | `pytest -m entity` / `-m control` / `-m boundary` | Layer 회귀 |
| REFACTOR 끝 | `pytest -q` (전체) | **Review Loop** — merge·보고 전 필수 |
| boundary 작업 후 | `pytest tests/boundary -q` | UI Track 격리 |
| 커밋 전(사용자 요청 시) | `pytest -q` | 전체 green 게이트 |

프로젝트 루트에서 실행. `pythonpath=src`는 `pyproject.toml`에 설정됨.

**Review Loop 완료 조건:** `pytest -q` exit 0, FR-T2 [reference.md](reference.md) `D-*` 구현·통과, ECB·Mock 위반 없음.

---

## 완료 보고 (매 Phase 종료 시)

한국어로 다음 항목을 bullet로 제출:

| # | 항목 |
|---|------|
| 1 | `Phase` / `Layer` / `Track` / 테스트 ID (`D-*` or `U-*`) |
| 2 | 변경 파일 목록 (`src/…`, `tests/…`) |
| 3 | 실행한 pytest 명령과 결과 (fail 수 / pass) |
| 4 | ECB·Mock·E00x 준수 여부 (위반 시 명시) |
| 5 | MagicConstant SSOT 준수 여부 |
| 6 | 다음 Phase 제안 (RED→GREEN→REFACTOR 중 하나) |
| 7 | FR-T2·PRD 매핑 (해당 시 S1/S2/S3 또는 FR-ID) |

**git commit/push:** 사용자 명시 요청 시에만.

---

## 추가 자료

- `D-*` 테스트 ID SSOT: [reference.md](reference.md)
- Command 스크립트: *(미도입 — 생성 금지)*
