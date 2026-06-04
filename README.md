# MagicSquare_xx

4×4 부분 마방진(빈칸 2, 합 34) **검증·풀이** CLI/모듈. ECB + Dual-Track TDD.

상세 요구: [`docs/PRD.md`](docs/PRD.md) · RED 설계·설계표: [`docs/TDD-RED-Todo.md`](docs/TDD-RED-Todo.md)

## 설치 · 테스트

```powershell
cd c:\DEV\MagicSquare_xx
python -m pip install -e ".[dev]"
python -m pytest -q
```

RED 단계에서는 각 항목 추가 후 **의도적 FAIL**을 확인한다 (`tests/`만 변경, `src/` 수정 금지).

---

## TDD RED 체크리스트

진행 시 `[ ]` → `[x]`로 갱신. 절차: [`.cursor/commands/tdd-red.md`](.cursor/commands/tdd-red.md)

### 선행 (fixture · 코드표)

- [ ] **G1** — 유효 부분 마방진 4×4 (`0`×2, 1~16 각 1회)
- [ ] **G_ok** — 완성 4×4 (빈칸 없음, 10조건 pass용)
- [ ] **E001~E007** 오류 코드표 `docs/`에 고정

### Track A — UI / Boundary (`tests/boundary/test_u_*.py`)

| 구분 | 할 일 |
|------|--------|
| 입력 | |
| | - [ ] **U-IN-01** — `grid=None` → `E003` `INVALID_NULL` (RED: `ModuleNotFoundError`) |
| | - [ ] **U-IN-02** — `grid=3×4` → `E001` `INVALID_SIZE` (RED: `AssertionError`) |
| | - [ ] **U-IN-03** — 빈칸 0개 → `E002` `INVALID_BLANKS` (RED: `AssertionError`) |
| 출력 | |
| | - [ ] **U-OUT-01** — 유효 입력 **G1** → `len(result)==6` (`int[6]`) (RED: `pytest.fail()`) |
| 플로우 | |
| | - [ ] **U-FLOW-02** — `grid=None` → `execute()` 0회, control 미호출 (RED: `pytest.fail()`) |
| 확장 | |
| | - [ ] **E004~E007** — `U-*` ID 매핑 확정 |
| | - [ ] **U-CLI-*** — `verify` CLI (stdin/파일, FR-C2~C4) |

```powershell
pytest tests/boundary -q
```

### Track B — Logic (`tests/entity/`, `tests/control/`)

Domain Mock 금지 · `MagicConstant` SSOT import만.

**entity** (`@pytest.mark.entity`)

- [ ] **D-CONST-SSOT** — `GRID_SIZE==4`, `TARGET_SUM==34`, `CELL_MAX==16`
- [ ] **D-VERIFY-OK-COMPLETE** — **G_ok** → 10조건 pass / `OK` (S1)
- [ ] **D-VERIFY-FAIL-MAIN-DIAG** — 행·열 OK, 주대각 NG → `FAIL` + `main_diagonal` (S3)
- [ ] **D-GRID-INVALID-DUPLICATE** — 1~16 중복 → `invalid grid`
- [ ] **D-GRID-INVALID-BLANKS-3** — `0` 3개 이상 → `invalid grid`
- [ ] **D-GRID-INCOMPLETE-2-BLANKS** — 빈칸 2 중간판 → FR-R6 `incomplete`/`skip`
- [ ] **D-SOLVE-INT6-1INDEX** — **G1** → `int[6]`, 좌표 1-index (1~4)

**control** (`@pytest.mark.control`)

- [ ] **D-CONTROL-VERIFY-GRID** — 완성 4×4 → `verify_grid(grid)` → **OK** (S1)

```powershell
pytest -m entity -q
pytest -m control -q
```

### RED 완료 게이트

- [ ] Track A `U-*` — `pytest tests/boundary -q` 의도적 FAIL 확인 → GREEN
- [ ] Track B `D-*` — `pytest -m entity -q` · `pytest -m control -q` 동일
- [ ] (GREEN·REFACTOR 후) `pytest -q` 전체 green
- [ ] ECB 리뷰 PASS — [`.cursor/commands/review-ecb.md`](.cursor/commands/review-ecb.md)

---

## 레이아웃

```
src/{entity,control,boundary}/
tests/{entity,control,boundary}/
docs/PRD.md
docs/TDD-RED-Todo.md
```
