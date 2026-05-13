# 🤖 VS Code Agent Mission — Chapter 1.2 HTML Conversion

## 임무 개요
아래 지시를 정확히 따라 `books.html` 파일의 챕터 1.2 본문 HTML을 생성하라.
**설명이나 부가적인 말 없이, 오직 완성된 HTML 코드만 출력하라.**

---

## 📂 읽어야 할 파일 (2개)

### 파일 1 — 변환 규칙서 (반드시 먼저 읽을 것)
```
C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr\mission_briefing_books.md
```
이 파일에 마크다운 → HTML 변환 규칙이 전부 정의되어 있다.

### 파일 2 — 변환할 원본 원고
```
C:\Obsidian_save\2026_Note\Adam_Samantha_Cozy_Place\02_book_projects\prompts_manuscript\1.2_토큰의_물리학.md
```
이 파일의 내용을 HTML로 변환해야 한다.

---

## 📋 출력 규칙

1. **규칙서(`mission_briefing_books.md`)의 모든 규칙을 적용**하여 원고를 HTML로 변환한다.
2. 출력 범위는 `<main class="chapter-content">` 안에 들어갈 **내부 HTML 스니펫**만이다. (`<main>` 태그 자체는 포함하지 않는다.)
3. 반드시 아래 순서를 지킨다:
   - `<div class="ch-eyebrow">` — "CHAPTER 1·2 · 무료 공개"
   - `<h1 class="ch-title">` — 원고의 챕터 제목
   - `<p class="ch-intro">` — 원고의 도입부 문단
   - `<div class="ch-body">` — 나머지 본문 전체 (소제목, 본문, 카드, 팁, callout 등)
   - `<hr class="ch-divider">` + `<ul class="checklist">` — 원고 마지막 체크리스트
   - `<div class="ch-nav">` — 네비게이션 (prev: 1.1절, next: 1.3절)
4. **절대 금지**: 인라인 스타일, 규칙서에 없는 클래스, 마크다운 문법 그대로 출력

---

## 📝 네비게이션 정보
- **이전**: `href="#ch1-1"` / 이름: `1.1 이중 번역의 늪`
- **다음**: `href="#ch1-3"` / 이름: `1.3 어텐션의 법칙`

---

## 🎯 최종 지시
1. `mission_briefing_books.md` 파일을 읽어 변환 규칙을 파악한다.
2. `1.2_토큰의_물리학.md` 파일을 읽어 원고 전체를 파악한다.
3. 규칙에 따라 HTML로 변환한다.
4. 결과물을 `C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr\ch1_2_output.html` 파일로 저장한다.
5. 완료 후 "변환 완료: ch1_2_output.html 저장됨" 이라고만 보고한다.
