"""
fix_ui_v2.py — Samantha.AI.kr 전체 UI 버그 수정
=================================================
수정 항목:
1. [전체] 햄버거 메뉴: z-index 수정 + 중복 제거 + JS 확실히 적용
2. [support.html] 중복 햄버거 제거 (SVG 버전 제거, span 버전만 유지)
3. [books.html] ▲▼ 스크롤 버튼 쌍 복구 (▼만 있던 문제)
4. [chapters] prev/next 경로 수정 (../../ -> ./)
5. [chapters] ▲▼ 스크롤 버튼 추가 (기존 ▲ 단독 → 쌍으로)
6. [chapters] 챕터5 반응형 CSS 이미 있는지 확인 후 처리
7. [전체] mobile-menu-overlay z-index를 700으로 올려 TOC(800) 바로 아래, 컨텐츠(500) 위에 배치
"""

import os
import re

ROOT = r"C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr"
CHAPTERS_DIR = os.path.join(ROOT, "convert", "html_output")

# ─────────────────────────────────────────────────────────────
# 1. mobile-menu-overlay z-index 수정 (400 → 700)
# ─────────────────────────────────────────────────────────────
OLD_OVERLAY_Z = "z-index: 400; opacity: 0;"
NEW_OVERLAY_Z = "z-index: 700; opacity: 0;"

# ─────────────────────────────────────────────────────────────
# 2. 스크롤 버튼 쌍 CSS (▲▼ 모두)
# ─────────────────────────────────────────────────────────────
SCROLL_BTNS_CSS = """
/* SCROLL BUTTONS PAIR */
#scroll-buttons {
  position: fixed; bottom: 30px; right: 20px;
  display: flex; flex-direction: column; gap: 8px;
  z-index: 900; opacity: 0; transform: translateY(20px);
  transition: all 0.3s; pointer-events: none;
}
#scroll-buttons.visible { opacity: 1; transform: translateY(0); pointer-events: auto; }
#scroll-buttons button {
  width: 44px; height: 44px; border-radius: 10px;
  background: var(--purple-dim, rgba(139,92,246,0.15));
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 0.5px solid var(--purple-border, rgba(139,92,246,0.3));
  color: var(--white, #f8f8ff); cursor: pointer;
  font-size: 16px; display: flex; align-items: center; justify-content: center;
  transition: background 0.3s, transform 0.2s;
}
#scroll-buttons button:hover { background: var(--purple, #8b5cf6); transform: scale(1.05); }
"""

SCROLL_BTNS_HTML = """<div id="scroll-buttons">
  <button onclick="window.scrollTo({top:0,behavior:'smooth'})" title="맨 위로">▲</button>
  <button onclick="window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})" title="맨 아래로">▼</button>
</div>"""

SCROLL_BTNS_JS = """
// Scroll Buttons Visibility
const _scrollBtns = document.getElementById('scroll-buttons');
if (_scrollBtns) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) _scrollBtns.classList.add('visible');
    else _scrollBtns.classList.remove('visible');
  });
}
"""

# ─────────────────────────────────────────────────────────────
# 3. 햄버거 메뉴 JS (확실히 동작하는 버전)
# ─────────────────────────────────────────────────────────────
HAMBURGER_JS = """
// Hamburger Menu
const _hamburger = document.getElementById('hamburger');
const _mobileMenu = document.getElementById('mobile-menu');
if (_hamburger && _mobileMenu) {
  _hamburger.addEventListener('click', () => {
    _hamburger.classList.toggle('active');
    _mobileMenu.classList.toggle('active');
    document.body.style.overflow = _mobileMenu.classList.contains('active') ? 'hidden' : '';
  });
  // Close on overlay click
  _mobileMenu.addEventListener('click', (e) => {
    if (e.target === _mobileMenu) {
      _hamburger.classList.remove('active');
      _mobileMenu.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
}
"""

def fix_file(filepath, is_chapter=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fname = os.path.basename(filepath)

    # ── 1. z-index 수정 (400 → 700)
    content = content.replace(OLD_OVERLAY_Z, NEW_OVERLAY_Z)

    # ── 2. support.html: 중복 햄버거 제거 (SVG 버전 제거)
    # onclick="toggleMobileMenu()" 버튼 + 구 모바일 메뉴 오버레이 제거
    if 'onclick="toggleMobileMenu()"' in content:
        # SVG 스타일 hamburger 버튼 제거
        content = re.sub(
            r'<button class="hamburger" onclick="toggleMobileMenu\(\)"[^>]*>.*?</button>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        # 구 mobile-overlay (id="mobileMenu") 제거
        content = re.sub(
            r'<!-- MOBILE MENU -->\s*<div class="mobile-overlay"[^>]*>.*?</div>\s*</div>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        # toggleMobileMenu 관련 JS 제거
        content = re.sub(
            r'function toggleMobileMenu\(\).*?(?=\n\s*(function|//|const|let|var|document|\}))',
            '',
            content,
            flags=re.DOTALL
        )

    # ── 3. 스크롤 버튼 처리
    # 기존 단독 #scroll-top 버튼 제거 후 쌍으로 교체
    has_scroll_btns = 'id="scroll-buttons"' in content

    if not has_scroll_btns:
        # 단독 scroll-top 버튼이 있으면 제거
        content = re.sub(
            r'<button id="scroll-top"[^>]*>.*?</button>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        # </body> 앞에 쌍 버튼 삽입
        content = content.replace('</body>', SCROLL_BTNS_HTML + '\n</body>')

        # CSS 추가 (</style> 앞)
        if '/* SCROLL BUTTONS PAIR */' not in content:
            content = content.replace('</style>', SCROLL_BTNS_CSS + '\n</style>')

    # ── 4. 스크롤 버튼 JS 및 햄버거 JS 확인
    # 기존 UI Logic for Scroll & Menu 제거 (중복 방지)
    content = re.sub(
        r'// UI Logic for Scroll &amp; Menu\n.*?(?=\n\s*\n)',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'// UI Logic for Scroll & Menu\n.*?(?=\n\s*\n)',
        '',
        content,
        flags=re.DOTALL
    )

    # JS 인젝션 - </script> 태그 마지막 것 앞에 삽입
    new_js_marker = '// === SAMANTHA UI v2 ==='
    if new_js_marker not in content:
        insert_js = f'{new_js_marker}\n{SCROLL_BTNS_JS}\n{HAMBURGER_JS}'
        # 마지막 </script> 앞에 삽입
        content = content[:content.rfind('</script>')] + insert_js + '\n</script>' + content[content.rfind('</script>')+9:]

    # ── 5. 챕터 파일: prev/next 경로 수정 (../../ → ./ 로 통일)
    if is_chapter:
        # ch-nav 내의 href에서 ../../ 제거하되, ../../index.html 같은 루트 링크는 유지
        def fix_chnav_href(m):
            href = m.group(1)
            # html_output 내 챕터 파일들은 같은 폴더에 있으므로 ../../ 제거
            if href.startswith('../../') and not any(href.endswith(x) for x in ['index.html', 'peh.html', 'ip.html', 'books.html', 'fna.html', 'support.html', 'guestbook.html', 'join.html', 'book_promotion.html']):
                href = './' + href[6:]
            return f'href="{href}"'

        # ch-nav 섹션에서만 패턴 적용
        def fix_chnav_section(m):
            return re.sub(r'href="([^"]+)"', fix_chnav_href, m.group(0))

        content = re.sub(
            r'<div class="ch-nav">.*?</div>',
            fix_chnav_section,
            content,
            flags=re.DOTALL
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {fname}")
    else:
        print(f"[SKIP]  {fname} (no changes)")


# ─── 루트 HTML 처리
print("\n=== ROOT HTML FILES ===")
for fname in os.listdir(ROOT):
    if fname.endswith('.html'):
        fix_file(os.path.join(ROOT, fname), is_chapter=False)

# ─── 챕터 HTML 처리
print("\n=== CHAPTER HTML FILES ===")
for fname in os.listdir(CHAPTERS_DIR):
    if fname.endswith('.html'):
        fix_file(os.path.join(CHAPTERS_DIR, fname), is_chapter=True)

print("\n[DONE] All fixes applied!")
