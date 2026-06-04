# MagicSquare_xx — TDD RED To Do List

**버전:** 0.1  
**작성일:** 2026-06-04  
**상태:** RED 설계 확정 · 테스트·구현 대기  
**근거:** Dual-Track RED 설계표, `.cursor/skills/magic-square-tdd/reference.md`, `docs/PRD.md` FR-T2

---

## 사용 방법

- 각 항목은 **RED 단계**에서 `tests/`에 실패 테스트를 추가할 때 체크한다.
- **GREEN/REFACTOR**는 본 문서 범위 밖 — 통과 후 별도 체크리스트로 관리.
- RED 실행: `.cursor/commands/tdd-red.md` · ID SSOT: `.cursor/skills/magic-square-tdd/reference.md`
- 완료 시 `[ ]` → `[x]`로 갱신.

**공통 fixture (미정의 시 선행):**

- [ ] **G1** — 유효 부분 마방진 4×4 (`0`×2, 1~16 각 1회) — `tests/conftest.py` 또는 track별 fixture
- [ ] **G_ok** — 완성 4×4 (빈칸 없음, 10조건 pass용)
- [ ] **E001~E007** 코드표를 `docs/`에 고정 (Report 02 리스크 대응)

---

## Track A — UI / Boundary (`U-*`)

**Layer:** `boundary` · **파일:** `tests/boundary/test_u_*.py` · **Marker:** `@pytest.mark.boundary`  
**Mock:** I/O·CLI Mock 허용 · **entity 직접 호출 금지**

### 입력 검증 (`U-IN`)

- [ ] **U-IN-01** — Given: `grid=None` → Then: `E003` `INVALID_NULL` → RED: `ModuleNotFoundError` · `test_u_*.py`
- [ ] **U-IN-02** — Given: `grid=3×4` → Then: `E001` `INVALID_SIZE` → RED: `AssertionError`
- [ ] **U-IN-03** — Given: 빈칸 0개 (`0` 없음) → Then: `E002` `INVALID_BLANKS` → RED: `AssertionError`

### 출력 계약 (`U-OUT`)

- [ ] **U-OUT-01** — Given: 유효 입력 **G1** → Then: `len(result)==6` (`int[6]`) → RED: `pytest.fail()` (의도적 RED)

### 플로우 / ECB (`U-FLOW`)

- [ ] **U-FLOW-02** — Given: `grid=None` → Then: `execute()` **0회** (control 미호출) → RED: `pytest.fail()`

### Boundary 확장 (미설계 — 추후 행 추가)

- [ ] **E004~E007** 매핑 및 대응 `U-*` ID 확정 후 본 섹션에 항목 추가
- [ ] **FR-C1** `verify` CLI — stdin/파일 입력 `U-CLI-*` (PRD FR-C2, FR-C3, FR-C4)

---

## Track B — Logic (`D-*`)

**Domain Mock 금지** (`patch`, 가짜 entity/control 금지) · 상수는 `MagicConstant` SSOT import만.

### entity — `tests/entity/test_d_*.py` · `@pytest.mark.entity`

- [ ] **D-CONST-SSOT** — Given: (구현 전) `MagicConstant` import → Then: `GRID_SIZE==4`, `TARGET_SUM==34`, `CELL_MAX==16` · RED: `ModuleNotFoundError` / `ImportError`
- [ ] **D-VERIFY-OK-COMPLETE** — Given: 완성 4×4 (**G_ok**, 빈칸 없음) → Then: 10조건 전부 pass / `OK` · RED: `ModuleNotFoundError` / `AssertionError` · PRD S1
- [ ] **D-VERIFY-FAIL-MAIN-DIAG** — Given: 행·열 합 34, 주대각선 ≠ 34 → Then: `FAIL` + `main_diagonal` · RED: `AssertionError` · PRD S3
- [ ] **D-GRID-INVALID-DUPLICATE** — Given: 1~16 중복 → Then: `invalid grid` · RED: `AssertionError` · FR-T2
- [ ] **D-GRID-INVALID-BLANKS-3** — Given: `0` 3개 이상 → Then: `invalid grid` · RED: `AssertionError` · FR-T2
- [ ] **D-GRID-INCOMPLETE-2-BLANKS** — Given: 빈칸 2개 중간판 → Then: FR-R6 `incomplete`/`skip` (정책 확정 후 assert 고정) · RED: `AssertionError` · FR-T2
- [ ] **D-SOLVE-INT6-1INDEX** — Given: **G1** (`0`×2) → Then: `int[6]` `[r1,c1,n1,r2,c2,n2]`, 좌표 1-index (1~4) · RED: `ModuleNotFoundError` / `AssertionError`

### control — `tests/control/test_d_*.py` · `@pytest.mark.control`

- [ ] **D-CONTROL-VERIFY-GRID** — Given: 완성 4×4 → `verify_grid(grid)` → Then: **OK** (entity 오케스트레이션) · RED: `ImportError` / `AssertionError` · PRD S1

---

## RED 설계표 (참고)

### Track A — Boundary

| Test ID | Given | Then (기대값) | Expected RED Failure |
| :--- | :--- | :--- | :--- |
| U-IN-01 | `grid=None` | E003 INVALID_NULL | ModuleNotFoundError |
| U-IN-02 | `grid=3×4` | E001 INVALID_SIZE | AssertionError |
| U-IN-03 | 빈칸 0개 | E002 INVALID_BLANKS | AssertionError |
| U-OUT-01 | 유효 입력 G1 | `len(result)==6` | pytest.fail() RED |
| U-FLOW-02 | `grid=None` | `execute()` 0회 | pytest.fail() RED |

### Track B — Logic (entity)

| Test ID | Given | Then (기대값) | Expected RED Failure |
| :--- | :--- | :--- | :--- |
| D-CONST-SSOT | MagicConstant import | 4 / 34 / 16 SSOT | ModuleNotFoundError / ImportError |
| D-VERIFY-OK-COMPLETE | G_ok 완성 4×4 | 10조건 pass / OK | ModuleNotFoundError / AssertionError |
| D-VERIFY-FAIL-MAIN-DIAG | 행·열 OK, 주대각 NG | FAIL + main_diagonal | AssertionError |
| D-GRID-INVALID-DUPLICATE | 1~16 중복 | invalid grid | AssertionError |
| D-GRID-INVALID-BLANKS-3 | `0`≥3 | invalid grid | AssertionError |
| D-GRID-INCOMPLETE-2-BLANKS | 빈칸 2 중간판 | incomplete/skip (FR-R6) | AssertionError |
| D-SOLVE-INT6-1INDEX | G1 | int[6], 1-index | ModuleNotFoundError / AssertionError |

### Track B — Logic (control)

| Test ID | Given | Then (기대값) | Expected RED Failure |
| :--- | :--- | :--- | :--- |
| D-CONTROL-VERIFY-GRID | 완성 4×4 | verify_grid → OK | ImportError / AssertionError |

---

## 완료 게이트 (Review Loop 전)

- [ ] Track A `U-*` RED 항목 전부: `pytest tests/boundary -q` — 의도적 FAIL 확인 후 GREEN 진행
- [ ] Track B `D-*` RED 항목 전부: `pytest -m entity -q` · `pytest -m control -q` — 동일
- [ ] `pytest -q` 전체 green (GREEN·REFACTOR 완료 후)
- [ ] ECB 리뷰: `.cursor/commands/review-ecb.md` 5항목 PASS

---

## 참고 문서

- `docs/PRD.md` — FR-T2, FR-R6, FR-C1~C4
- `.cursorrules` — ECB, Dual-Track, E001~E007
- `.cursor/skills/magic-square-tdd/SKILL.md` — RED/GREEN/REFACTOR 절차
- `Report/02.Project-Bootstrap-Report.md` — Harness 상태
