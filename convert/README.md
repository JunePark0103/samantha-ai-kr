# MD → HTML 변환기 사용 설명

## 폴더 구조 (권장)

```
내_프로젝트/
│
├── chapters/              ← ★ .md 파일 여기에 넣기
│   ├── 01_intro.md
│   ├── 02_chapter.md
│   └── ...
│
├── html_output/           ← 변환된 .html이 자동 생성됨
│   ├── 01_intro.html
│   ├── 02_chapter.html
│   └── ...
│
├── css/
│   └── style.css          ← 네 CSS 파일 (또는 sample_style.css 복사)
│
├── convert.py             ← 변환 스크립트
└── 변환시작.bat            ← ★ 더블클릭으로 실행
```

---

## 사용법

1. `chapters/` 폴더에 `.md` 파일 넣기
2. `변환시작.bat` 더블클릭
3. `html_output/` 폴더에 완성된 `.html` 확인

---

## convert.py 설정값 (상단에서 수정)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MD_FOLDER` | `./chapters` | .md 파일이 있는 폴더 |
| `OUTPUT_FOLDER` | `./html_output` | 변환된 .html 저장 위치 |
| `CSS_PATH` | `../css/style.css` | HTML에서 참조할 CSS 경로 |
| `SITE_TITLE` | `나의 책` | 사이트/탭 제목 |
| `SHOW_NAV` | `True` | 이전/다음 챕터 링크 표시 여부 |

---

## MD 파일 챕터 순서 맞추기

파일명 앞에 번호를 붙이면 자동으로 순서대로 정렬돼:

```
01_들어가며.md
02_1장_배경.md
03_2장_본론.md
04_마치며.md
```

---

## 내 CSS 연결 방법

1. 네 CSS 파일을 `css/` 폴더에 저장
2. `convert.py` 상단의 `CSS_PATH` 경로를 네 CSS 파일로 변경
3. 다시 `변환시작.bat` 실행 → 전체 재변환

---

## 지원하는 마크다운 문법

- 제목 `# ## ###`
- **굵게**, *기울임*, ~~취소선~~
- 표 `| col | col |`
- 코드 블록 (인라인 + 펜스)
- 인용문 `>`
- 각주 `[^1]`
- 이미지 `![alt](path)`
- 링크 `[텍스트](url)`
- 목록 (순서 있음/없음)
- 수평선 `---`
