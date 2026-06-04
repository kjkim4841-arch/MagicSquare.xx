# Review ECB — 계약·레이어 위반만

MagicSquare_1004 **ECB·계약 리뷰**. **코드 수정 금지** (read/search만). 헌법: `.cursorrules`, `docs/PRD.md`.

---

## 필수 선언

응답 **첫 줄**:

```
Phase: review | Scope: ECB+contract | Mode: read-only
```

---

## 절차

1. **범위** — 사용자가 지정한 경로·커밋·브랜치; 없으면 `src/`, `tests/` 전체.
2. **수집** — `grep`/파일 읽기로 import, `E00`, `34`/`16`, `mock`/`patch`, `int[6]`·좌표 사용처 목록화.
3. **판정** — 아래 5개 체크 항목별 **PASS / FAIL / N/A** (코드 없으면 N/A).
4. **표만 출력** — 위반 행만 상세; PASS는 한 줄 요약 가능.
5. **금지** — 수정·포맷·리팩터·테스트 추가·commit/push 제안 실행.

---

## 체크 항목 (헌법)

| # | 체크 | PASS 기준 |
|---|------|-----------|
| 1 | **import 방향** | `boundary→control→entity`만; `entity`가 `control`/`boundary` import 없음; `control`이 `boundary` import 없음; `boundary`가 `entity` 직접 import 없음 |
| 2 | **entity E001~E005** | `src/entity`에 `E001`~`E005` 문자열·발생·매핑·CLI exit 처리 없음 (도메인 결과 타입만) |
| 3 | **int[6] 1-index** | 솔버 성공 계약 `[r1,c1,n1,r2,c2,n2]`; 행·열 **1~4** (0-index API 노출 없음) |
| 4 | **MagicConstant SSOT** | `34`/`16`/`4` 리터럴이 `src/entity` SSOT 외 `src/`·`tests/`에 산재 없음 (테스트는 SSOT import) |
| 5 | **Logic Track Domain Mock** | `tests/entity`, `tests/control`, `test_d_*`에 `patch`/가짜 entity·domain 우회 Mock 없음 |

**부가 계약 (FAIL 시 표에 포함):**

- 검증 CLI 출력은 PRD `OK`/`FAIL` (boundary); 솔버는 `int[6]` — **혼용 금지**
- `E006`~`E007`은 boundary; entity에서 **모든 E00x** 처리 금지 권장

---

## 리뷰 결과 표 (필수 형식)

### 요약

| 체크 | 결과 | 위반 수 |
|------|------|--------|
| import 방향 | PASS / FAIL / N/A | |
| entity E001~E005 | PASS / FAIL / N/A | |
| int[6] 1-index | PASS / FAIL / N/A | |
| MagicConstant SSOT | PASS / FAIL / N/A | |
| Logic Domain Mock | PASS / FAIL / N/A | |

### 위반 상세 (FAIL만)

| 체크 | 파일:줄 | 관측 | 계약 |
|------|---------|------|------|
| *(예)* import 방향 | `src/entity/foo.py:3` | `from boundary import …` | entity→* 금지 |

위반 0건이면: `위반 없음 — 5항목 PASS`.

---

## 보고

한국어. **표 2개(요약·위반)** + 검토 파일 수 1줄. 수정 패치·구현 제안은 **사용자 요청 시에만** 별도.

---

## 금지

- **모든 코드·설정 수정** (`src/`, `tests/`, `pyproject.toml` 등).
- 위반을 고치기 위한 자동 편집·커밋.
- 리뷰 없이 TDD Phase 진행.
