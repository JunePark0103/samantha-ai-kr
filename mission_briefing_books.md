# 🎯 Books 페이지 마크다운 변환 지시서 (Mission Briefing)

당신은 이제부터 제가 제공하는 방대한 원고 텍스트를 `Samantha.AI` 웹사이트의 `books.html` 구조와 CSS에 완벽하게 호환되는 **고급 마크다운(HTML 혼합) 포맷**으로 변환하는 역할을 수행합니다.

아래의 엄격한 클래스 규칙과 템플릿을 준수하여 텍스트를 변환해 주세요.

---

## 🛑 [필수 준수 규칙]

### 1. 기본 본문 텍스트 (ch-body)
- **일반 문단**: 일반 텍스트로 작성하면 스크립트가 자동으로 `<p>` 태그로 변환합니다. (엔터 두 번으로 단락 구분)
- **소제목**: `##` (`<h2>`) 또는 `###` (`<h3>`)를 사용하세요. (CSS에서 자동으로 `—` 기호나 색상이 적용되도록 세팅되어 있습니다.)
- **강조**: `**강조어**` (`<strong>`) 또는 `*단어*` (`<em>`)를 사용하세요.

### 2. 인용구 및 인사이트 (Callout)
중요한 경고나 아키텍트의 통찰력, 팁 등을 표현할 때는 아래 HTML을 **그대로** 복사하여 내용만 교체하세요.

```html
<div class="callout">
  <div class="callout-label">아키텍트 인사이트: 뉘앙스의 증발</div>
  <p>여기에 본문 내용을 작성하세요.</p>
</div>
```
*(주의: `callout-label`에는 "아키텍트의 경고", "인사이트" 등의 라벨을 적어줍니다.)*

### 3. 번호가 매겨진 핵심 카드 (AI Architect Card)
'구조', '설계 가이드' 등 구획을 나누어 세련되게 보여주어야 하는 박스형 콘텐츠는 아래 형태를 사용합니다.

```html
<div class="ai-architect-card">
  <div class="card-number">01</div>
  <div class="card-title">이중 번역 (Double Translation)의 구조</div>
  <div class="card-content">
    <ol>
      <li><strong>의도(Intent)의 왜곡</strong>: 당신의 생각이 번역되는 과정입니다.</li>
      <li><strong>지능(Intelligence)의 파편화</strong>: 문장이 벡터로 번역되는 과정입니다.</li>
    </ol>
  </div>
</div>
```

### 4. 사만다의 꿀팁 (Sparkling Tip)
본문 중간에 가볍게 들어가는 실전 팁이나 '사만다의 조언' 파트입니다.

```html
<div class="sparkling-tip">
  <div class="tip-icon">💡</div>
  <div class="tip-body">
    <p><strong>Sparkling Tip #1</strong>: 여기에 팁의 세부 내용을 작성하세요.</p>
  </div>
</div>
```

### 5. 챕터 마무리의 체크리스트 (Checklist)
각 장이 끝날 때 독자가 확인해야 할 최종 체크리스트 영역입니다.

```html
<div class="ch-divider"></div>

<div class="callout" style="background: var(--teal-dim); border-color: var(--teal-border); border-left-color: var(--teal);">
  <div class="callout-label" style="color: var(--teal);">1.1절 완결: 아키텍트의 최종 체크리스트</div>
  <ul class="checklist" style="background: transparent; border: none; padding: 0; margin-top: 10px;">
    <li><input type="checkbox"> <span>내 프롬프트에 '모호한 형용사'가 없는가</span></li>
    <li><input type="checkbox"> <span>3대 좌표가 명시되었는가</span></li>
  </ul>
</div>
```

---

## ⚡ [변환 시 주의사항]
- **절대 `<main class="chapter-content">`나 `<article>` 등 최상위 태그를 임의로 덮어씌우지 마세요.** 오직 **내부 콘텐츠**에 들어갈 내용만 작성해야 합니다.
- 불필요하게 모든 문장을 `<div>`로 감싸지 말고, 문단은 순수 마크다운 텍스트로 두어 가독성을 높이세요.
- 제공된 원고의 내용, 뉘앙스, 문체를 절대 임의로 요약하거나 삭제하지 말고 100% 반영하세요.

위 지침을 숙지했다면, 이제부터 제가 전달하는 원고를 변환해 주시면 됩니다.
