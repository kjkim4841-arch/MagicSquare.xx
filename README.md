# MagicSquare_xx

4×4 부분 마방진(빈칸 2, 합 34) **검증·풀이** CLI/모듈. **ECB** + **Dual-Track TDD**.

| 문서 | 용도 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 제품 요구·FR·성공 기준 |
| [`docs/TDD-RED-Todo.md`](docs/TDD-RED-Todo.md) | RED 설계·체크리스트 SSOT |
| [`.cursorrules`](.cursorrules) | ECB·Mock·상수 SSOT 헌법 |
| [`.cursor/skills/magic-square-tdd/`](.cursor/skills/magic-square-tdd/) | RED/GREEN/REFACTOR 절차 |

---

## 현재 상태 (2026-06-04)

| 항목 | 상태 |
|------|------|
| **pytest** | `2 passed` — `D-LOC-01`, `D-SOL-01` (entity Logic) |
| **entity** | `MagicConstant`, `find_blank_coords`, `solve_step_a` |
| **control / boundary** | 스켈레톤만 (`__init__.py`) |
| **다음 REFACTOR** | P0: `tests/_approval.py:assert_matches_golden` 분리 — [`Report/04.Refactor-Smell-Report.md`](Report/04.Refactor-Smell-Report.md) |

```powershell
cd c:\DEV\MagicSquare_xx
python -m pip install -e ".[dev]"
python -m pytest -q          # 전체 (현재 2)
python -m pytest -m entity -q
```

---

## 설치 · 테스트

```powershell
cd c:\DEV\MagicSquare_xx
python -m pip install -e ".[dev]"
python -m pytest -v
```

- `pythonpath=src` — [`pyproject.toml`](pyproject.toml)
- **Logic Track** (`test_d_*`): Domain Mock 금지 · `MagicConstant` SSOT import
- **UI Track** (`test_u_*`): I/O·CLI Mock 허용 · boundary→control만

**Golden Master** (`tests/_approval.py`, `tests/golden/`):

```powershell
# 승인 텍스트 갱신 시에만 (사용자 명시 승인 후)
$env:UPDATE_GOLDEN="1"
python -m pytest tests/entity/test_d_sol_01.py -v
```

---

## ECB 레이어

```
boundary ──► control ──► entity
```

| Layer | 역할 | 현재 |
|-------|------|------|
| **entity** | 격자·합 34·검증/솔루션 순수 로직, E001~E005 없음 | `constants`, `loc`, `solve` |
| **control** | 유스케이스 조율, entity만 호출 | 미구현 |
| **boundary** | CLI·E001~E007·exit code | 미구현 |

**계약:** 검증 CLI → `OK` / `FAIL … expected=34` · 솔버 성공 → `int[6]` `[r1,c1,n1,r2,c2,n2]` (좌표 **1-index**)

---

## TDD 진행 체크리스트

진행 시 `[ ]` → `[x]`로 갱신. RED 절차: [`.cursor/commands/tdd-red.md`](.cursor/commands/tdd-red.md) · ECB 리뷰: [`.cursor/commands/review-ecb.md`](.cursor/commands/review-ecb.md)

### 선행 (fixture · 코드표)

- [x] **G1** — `tests/conftest.py` · `grid_g1` (0×2, 1~16 각 1회)
- [ ] **G_ok** — 완성 4×4 (빈칸 없음, 10조건 pass용)
- [ ] **E001~E007** 오류 코드표 `docs/`에 고정

### Track A — UI / Boundary (`tests/boundary/test_u_*.py`)

| 구분 | 할 일 |
|------|--------|
| 입력 | |
| | - [ ] **U-IN-01** — `grid=None` → `E003` `INVALID_NULL` |
| | - [ ] **U-IN-02** — `grid=3×4` → `E001` `INVALID_SIZE` |
| | - [ ] **U-IN-03** — 빈칸 0개 → `E002` `INVALID_BLANKS` |
| 출력 | |
| | - [ ] **U-OUT-01** — **G1** → `len(result)==6` (`int[6]`) |
| 플로우 | |
| | - [ ] **U-FLOW-02** — `grid=None` → control 미호출 |
| 확장 | |
| | - [ ] **E004~E007** — `U-*` ID 매핑 |
| | - [ ] **U-CLI-*** — `verify` CLI (FR-C2~C4) |

```powershell
pytest tests/boundary -q
```

### Track B — Logic (`tests/entity/`, `tests/control/`)

**entity** (`@pytest.mark.entity`)

- [x] **D-CONST-SSOT** — `src/entity/constants.py` · `MagicConstant` (4 / 16 / 34 / 0)
- [x] **D-LOC-01** — **G1** → `find_blank_coords` → `[(2,2),(3,3)]` row-major 1-index (`test_d_loc_01.py`)
- [x] **D-SOL-01** (step A) — **G1** → `solve_step_a` → `int[6]` + Golden (`test_d_sol_01.py`)
- [ ] **D-LOC-02** · **D-LOC-03** — 좌표 범위·길이 불변 (미작성)
- [ ] **D-VERIFY-OK-COMPLETE** — **G_ok** → 10조건 pass / `OK` (S1)
- [ ] **D-VERIFY-FAIL-MAIN-DIAG** — 행·열 OK, 주대각 NG → `FAIL` + `main_diagonal` (S3)
- [ ] **D-GRID-INVALID-DUPLICATE** — 1~16 중복 → `invalid grid`
- [ ] **D-GRID-INVALID-BLANKS-3** — `0` 3개 이상 → `invalid grid`
- [ ] **D-GRID-INCOMPLETE-2-BLANKS** — 빈칸 2 중간판 → FR-R6 `incomplete`/`skip`
- [ ] **D-SOLVE-INT6-1INDEX** — 솔버 전체 계약 (step A만 부분 충족)

**control** (`@pytest.mark.control`)

- [ ] **D-CONTROL-VERIFY-GRID** — 완성 4×4 → `verify_grid(grid)` → **OK** (S1)

```powershell
pytest -m entity -q
pytest -m control -q
```

### 게이트

- [ ] Track A `U-*` — boundary RED → GREEN
- [x] Track B 일부 — `D-LOC-01`, `D-SOL-01` GREEN (`pytest -m entity` 2 passed)
- [ ] (완료 시) `pytest -q` 전체 green + FR-T2 `D-*` 전부
- [ ] ECB 리뷰 PASS — [`.cursor/commands/review-ecb.md`](.cursor/commands/review-ecb.md)

RED 단계에서는 **의도적 FAIL** 확인 후 GREEN. REFACTOR는 green 유지하며 구조만 변경.

---

## 레이아웃

```
src/
  entity/          constants.py, loc.py, solve.py
  control/         (스켈레톤)
  boundary/        (스켈레톤)
tests/
  conftest.py      grid_g1 (G1)
  _approval.py     Golden Master 헬퍼
  golden/          승인 텍스트 스냅샷
  entity/          test_d_loc_01.py, test_d_sol_01.py
  control/         (대기)
  boundary/        (대기)
docs/              PRD.md, TDD-RED-Todo.md
Report/            세션 보고서 (01~04)
Prompting/         Export Transcript (01~04)
.cursor/           rules, skills, commands
```

---

## 세션 기록

| # | 보고서 | Transcript |
|---|--------|------------|
| 01 | Mom Test · 문제 정의 | `01.Mom-Test-STEP1-*` |
| 02 | Project Bootstrap | `02.Project-Bootstrap-*` |
| 03 | D-LOC-01 RED | `03.D-LOC-01-RED-*` |
| 04 | REFACTOR Smell Scan | `04.Refactor-Smell-*` |
