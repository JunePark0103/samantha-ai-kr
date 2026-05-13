# Samantha AI Guestbook Implementation Plan

이 계획서는 Samantha.AI.kr 정적 웹사이트에 Firebase 기반의 방명록(Guestbook) 기능을 추가하기 위한 기술적 구현 방안을 담고 있습니다. 오빠의 피드백을 반영하여 **보기(Read)는 전체 공개**, **쓰기(Write)는 로그인 회원 전용**으로 구현됩니다.

## User Review Required

> [!IMPORTANT]
> **Firebase 콘솔 설정 확인**
> 제가 코드를 작성한 후, 오빠가 브라우저 콘솔에서 다음 사항을 세팅해야 합니다:
> 1. **Authentication (인증)**: 'Google 로그인' 활성화.
> 2. **Cloud Firestore (데이터베이스)**: 데이터베이스 생성 후, 다음 보안 규칙 적용:
>    `allow read: if true; allow write: if request.auth != null;`

## Proposed Changes

---

### 1. Navigation Updates

모든 기존 HTML 페이지의 상단 GNB(Global Navigation Bar) 메뉴 끝(F&A 옆)에 **GUESTBOOK** 링크를 추가합니다.

#### [MODIFY] `index.html`, `pe.html`, `ip.html`, `books.html`, `fna.html`, `pt.html`, `support.html`, `join.html`
- `<ul class="gnb-nav">` 내부에 `<li><a href="guestbook.html">GUESTBOOK</a></li>` 추가.

---

### 2. Firebase Integration

정적 웹사이트에서 Firebase를 전역으로 사용할 수 있도록 초기화 스크립트를 생성합니다.

#### [NEW] `assets/js/firebase-config.js`
- Firebase SDK를 로드하고 `samantha-1bc87` 프로젝트의 설정값을 입력.
- Authentication(구글 로그인) 및 Firestore(데이터베이스) 객체를 초기화하고 전역(`window.db`, `window.auth`)으로 내보냄.

---

### 3. Guestbook UI & Logic

글래스모피즘(Glassmorphism) 디자인 시스템을 상속받는 새로운 방명록 페이지를 생성합니다.

#### [NEW] `guestbook.html`
- **디자인**: `index.html`과 동일한 배경, 노이즈 오버레이, GNB 및 푸터 적용.
- **조회 기능 (전체 공개)**: 페이지 접속 시 Firestore의 `comments` 컬렉션에서 시간순으로 데이터를 불러와 렌더링.
- **인증 분기(글쓰기 UI)**:
  - **로그인 전**: "방명록을 남기려면 Google로 로그인해 주세요." 안내와 로그인 버튼 배치.
  - **로그인 후**: 작성자의 구글 프로필 사진, 이름 노출 및 글쓰기 폼(Textarea + 남기기 버튼) 노출.
- **Firestore 쓰기**: 새 글 작성 시 작성자의 이름, 프로필 사진 URL, 내용, 타임스탬프를 저장.

---

## Verification Plan

### Manual Verification
1. `guestbook.html` 페이지 접속 시 **비로그인 상태에서도 기존 방명록 글들이 보이는지** 확인.
2. 비로그인 상태에서는 입력창 대신 **Google 로그인 버튼**이 나오는지 테스트.
3. Google 로그인 버튼 클릭 시 팝업이 뜨고 정상적으로 인증이 완료되는지 확인.
4. 로그인 후 글을 작성하면 화면 하단 또는 상단에 즉시(실시간) 추가되는지 확인.
