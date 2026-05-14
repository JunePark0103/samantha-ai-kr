"""
fix_orphan.py
==============
fix_ui_v2.py 가 만든 고아 DOMContentLoaded 블록만 정확히 제거.
제거 대상 패턴 (index.html/samantha.html 이미 수동 수정됨):

    (빈 줄 여러 개)
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobile-menu');
      if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', () => {
          hamburger.classList.toggle('active');
          mobileMenu.classList.toggle('active');
          document.body.style.overflow = ...;
        });
      }
    });     <-- 고아 DOMContentLoaded 닫기

다른 코드는 절대 건드리지 않는다.
"""

import os
import re

ROOT = r"C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr"
CHAPTERS = os.path.join(ROOT, "convert", "html_output")

# 이미 수동 수정된 파일은 건너뜀
ALREADY_FIXED = {"index.html", "samantha.html"}

# 고아 블록 패턴 (줄바꿈 형식 \r\n 고려)
ORPHAN_PATTERN = re.compile(
    r'\r?\n\r?\n\r?\n'                         # 빈 줄 2~3개
    r'  const hamburger = document\.getElementById\(\'hamburger\'\);'
    r'\r?\n'
    r'  const mobileMenu = document\.getElementById\(\'mobile-menu\'\);'
    r'\r?\n'
    r'  if \(hamburger && mobileMenu\) \{'
    r'\r?\n'
    r'    hamburger\.addEventListener\(\'click\', \(\) => \{'
    r'\r?\n'
    r'      hamburger\.classList\.toggle\(\'active\'\);'
    r'\r?\n'
    r'      mobileMenu\.classList\.toggle\(\'active\'\);'
    r'\r?\n'
    r'      document\.body\.style\.overflow = .*?;'
    r'\r?\n'
    r'    \}\);'
    r'\r?\n'
    r'  \}'
    r'\r?\n'
    r'\}\);',
    re.DOTALL
)

def fix_file(path):
    fname = os.path.basename(path)
    if fname in ALREADY_FIXED:
        print(f"[SKIP-manual] {fname}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, count = ORPHAN_PATTERN.subn('', content)

    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[FIXED x{count}] {fname}")
    else:
        print(f"[SKIP]         {fname}")

print("=== ROOT FILES ===")
for fname in os.listdir(ROOT):
    if fname.endswith('.html'):
        fix_file(os.path.join(ROOT, fname))

print("\n=== CHAPTER FILES ===")
for fname in os.listdir(CHAPTERS):
    if fname.endswith('.html'):
        fix_file(os.path.join(CHAPTERS, fname))

print("\n[DONE]")
