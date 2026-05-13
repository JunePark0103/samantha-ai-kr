import os
import re

html_dir = r"C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr"
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]

# The mobile menu logic
mobile_menu_html = """
<!-- MOBILE MENU OVERLAY -->
<div class="mobile-menu-overlay" id="mobile-menu">
  <div class="mobile-menu-inner">
    <a href="peh.html">PEH</a>
    <a href="ip.html">IP</a>
    <a href="books.html">BOOKS</a>
    <a href="fna.html">F&A</a>
    <a href="support.html">SUPPORT</a>
    <a href="guestbook.html">GUESTBOOK</a>
    <a href="join.html" class="mobile-cta">회원가입</a>
  </div>
</div>
"""

scroll_btns_html = """
<div id="scroll-buttons">
  <button id="scroll-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="맨 위로">▲</button>
  <button id="scroll-bottom" onclick="window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})" title="맨 아래로">▼</button>
</div>
"""

scroll_css = """
/* SCROLL BUTTONS */
#scroll-buttons {
  position: fixed; bottom: 30px; right: 30px;
  display: flex; flex-direction: column; gap: 8px;
  z-index: 900; opacity: 0; transform: translateY(20px);
  transition: all 0.3s; pointer-events: none;
}
#scroll-buttons.visible { opacity: 1; transform: translateY(0); pointer-events: auto; }
#scroll-buttons button {
  width: 48px; height: 48px; border-radius: 12px;
  background: var(--purple-dim, rgba(139,92,246,0.15));
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 0.5px solid var(--purple-border, rgba(139,92,246,0.3));
  color: var(--white, #f8f8ff); cursor: pointer;
  font-size: 16px; display: flex; align-items: center; justify-content: center;
  transition: background 0.3s, transform 0.2s;
}
#scroll-buttons button:hover { background: var(--purple, #8b5cf6); transform: scale(1.05); }

/* MOBILE MENU & OVERLAY */
.hamburger { display: none; background: none; border: none; cursor: pointer; padding: 10px; z-index: 600; }
.hamburger span { display: block; width: 24px; height: 2px; background: var(--white, #f8f8ff); margin: 5px 0; transition: 0.3s; border-radius: 2px; }
.hamburger.active span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger.active span:nth-child(2) { opacity: 0; }
.hamburger.active span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

.mobile-menu-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: rgba(7,7,15,0.95); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); z-index: 400; opacity: 0; pointer-events: none; transition: opacity 0.4s ease; display: flex; align-items: center; justify-content: center; }
.mobile-menu-overlay.active { opacity: 1; pointer-events: auto; }
.mobile-menu-inner { display: flex; flex-direction: column; align-items: center; gap: 24px; transform: translateY(20px); transition: transform 0.4s ease; }
.mobile-menu-overlay.active .mobile-menu-inner { transform: translateY(0); }
.mobile-menu-inner a { color: var(--white, #f8f8ff); text-decoration: none; font-size: 20px; font-weight: 600; font-family: 'Noto Serif KR', serif; letter-spacing: 0.05em; transition: color 0.2s; }
.mobile-menu-inner a:hover { color: var(--purple, #8b5cf6); }
.mobile-cta { margin-top: 10px; background: #f97316 !important; padding: 12px 32px; border-radius: 30px; border: 1px solid #fff; font-size: 16px; font-weight: 700; color: #fff !important; }

@media (max-width: 768px) {
  .gnb-nav, .gnb-cta { display: none !important; }
  .hamburger { display: block !important; }
}
"""

scroll_js = """
// UI Logic for Scroll & Menu
document.addEventListener('DOMContentLoaded', () => {
  const scrollBtns = document.getElementById('scroll-buttons');
  if (scrollBtns) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) scrollBtns.classList.add('visible');
      else scrollBtns.classList.remove('visible');
    });
  }

  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });
  }
});
"""

for f in html_files:
    filepath = os.path.join(html_dir, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False

    # 1. Update footer logo to be a link
    if '<div class="footer-logo">Samantha<em>.AI</em></div>' in content:
        content = content.replace('<div class="footer-logo">Samantha<em>.AI</em></div>', '<a href="index.html" class="footer-logo" style="text-decoration: none;">Samantha<em>.AI</em></a>')
        modified = True
    elif '<a href="index.html" class="footer-logo">Samantha<em>.AI</em></a>' in content:
        # Just to ensure text-decoration: none if not present
        content = content.replace('<a href="index.html" class="footer-logo">Samantha<em>.AI</em></a>', '<a href="index.html" class="footer-logo" style="text-decoration: none;">Samantha<em>.AI</em></a>')
        modified = True
        
    # 2. Add scroll buttons
    if 'id="scroll-buttons"' not in content:
        # replace old scroll-top if exists
        content = re.sub(r'<button id="scroll-top".*?</button>', '', content)
        content = content.replace('</body>', scroll_btns_html + '\n</body>')
        modified = True

    # 3. Add mobile overlay
    if 'id="mobile-menu"' not in content:
        content = content.replace('</nav>', '</nav>\n' + mobile_menu_html)
        modified = True
        
    # 4. Add hamburger to GNB
    if 'id="hamburger"' not in content:
        hamburger_btn = '  <button class="hamburger" id="hamburger" aria-label="메뉴 열기">\n    <span></span><span></span><span></span>\n  </button>\n</nav>'
        content = content.replace('</nav>', hamburger_btn)
        # remove double </nav> if it happened
        content = content.replace('</nav>\n</nav>', '</nav>')
        modified = True

    # 5. Add CSS
    if '/* SCROLL BUTTONS */' not in content:
        content = content.replace('</style>', scroll_css + '\n</style>')
        modified = True

    # 6. Add JS
    if 'UI Logic for Scroll & Menu' not in content:
        if '<script>' in content:
            content = content.replace('</script>', scroll_js + '\n</script>')
        else:
            content = content.replace('</body>', '<script>\n' + scroll_js + '\n</script>\n</body>')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")

print("Done updating HTML files.")
