# D-* 테스트 ID (Logic Track)

FR-T2·PRD S1~S3 매핑. 파일명 예: `test_d_<slug>.py`.

| ID | 케이스 | 기대 |
|----|--------|------|
| `D-VERIFY-OK-COMPLETE` | 완성 4×4 (빈칸 없음) | 10조건 pass / OK |
| `D-VERIFY-FAIL-MAIN-DIAG` | 행·열 OK, 주대각 NG | FAIL + main_diagonal |
| `D-GRID-INVALID-DUPLICATE` | 1~16 중복 | invalid grid |
| `D-GRID-INVALID-BLANKS-3` | `0` 3개 이상 | invalid grid |
| `D-GRID-INCOMPLETE-2-BLANKS` | 빈칸 2개 중간판 | incomplete/skip (FR-R6 확정 후 assert 고정) |
| `D-CONST-SSOT` | MagicConstant | 34/16/4 리터럴 산재 없음 |
| `D-SOLVE-INT6-1INDEX` | 솔버 성공 | `int[6]`, 좌표 1-index |

`control` 오케스트레이션: `D-CONTROL-VERIFY-GRID` (Skill API `verify_grid`).
