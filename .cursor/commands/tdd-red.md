# TDD RED — 실패 테스트 먼저

MagicSquare_1004 **Dual-Track TDD** — **RED 단계만**. 헌법: `.cursorrules`. `D-*` ID: `.cursor/skills/magic-square-tdd/reference.md`.

---

## 필수 선언

응답 **첫 줄** (고정 형식):

```
Phase: red | Layer: <entity|control|boundary> | Track: <Logic|UI> (<D-*|U-*>)
```

예:

```
Phase: red | Layer: entity | Track: Logic (D-VERIFY-FAIL-MAIN-DIAG)
```

```
Phase: red | Layer: boundary | Track: UI (U-CLI-VERIFY-STDIN)
```

---

## 절차

1. **ID 확인** — `D-*`(Logic) 또는 `U-*`(UI)를 [reference.md](../skills/magic-square-tdd/reference.md)에서 고르거나 사용자 지정 ID를 명시.
2. **파일 위치** — Logic: `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py` + `@pytest.mark.entity` / `control`. UI: `tests/boundary/test_u_*.py` + `@pytest.mark.boundary`.
3. **AAA 테스트** — Arrange(격자·fixture) → Act(호출 대상 **시그니처만**, 구현 없음) → Assert(기대 1개 이상, **엄격**).
4. **상수** — `34`/`16`/`4` 리터럴 금지; RED에서도 `MagicConstant` SSOT **import만** 허용(모듈 없으면 테스트가 import error로 FAIL해도 됨).
5. **pytest FAIL** — 아래 bash로 실행, **실패 확인** 후 보고. 통과하면 RED 아님 → assert/기대값 재검토.

---

## pytest 예시 (bash)

프로젝트 루트:

```bash
# Logic — entity 단일 파일
pytest tests/entity/test_d_verify_fail_main_diag.py -q

# Logic — control
pytest tests/control/test_d_control_verify_grid.py -q

# Layer marker
pytest -m entity -q
pytest -m control -q

# UI — boundary
pytest tests/boundary/test_u_cli_verify_stdin.py -q
pytest -m boundary -q
```

**기대:** exit code ≠ 0, `FAILED` 또는 `ERROR` (구현 부재·의도적 assert 실패).

---

## 보고

한국어 bullet:

| 항목 | 내용 |
|------|------|
| 테스트 ID | `D-*` 또는 `U-*` |
| FAIL 요약 | pytest 마지막 5~10줄 또는 실패 유형 1문장 |
| 변경 파일 | **`tests/`만** (경로 전체) |

다음 제안 한 줄: `Phase: green | Layer: … | Track: …`

---

## 금지

- **`src/` 수정** — 구현·스텁·`__init__` export 추가 금지 (GREEN까지).
- **Logic Track Domain Mock** — `unittest.mock.patch`, 가짜 entity/control, I/O fixture로 도메인 우회 금지.
- **assert 완화** — 기대값 느슨하게 변경, `pytest.skip` / `xfail`, 테스트 삭제.
- **Phase 넘김** — FAIL 확인 전 GREEN/REFACTOR 금지.
- **git commit/push** — 사용자 명시 요청 시에만.
