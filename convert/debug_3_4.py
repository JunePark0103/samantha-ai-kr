import os
import re
import markdown
from markdown.extensions.toc import TocExtension

def preprocess_samantha_tags(md_text):
    # 1. Callout 변환 (> [!NOTE] 등) - 내용 앞의 '>' 제거 보강
    def repl_callout(match):
        type_str = match.group(1).upper()
        content = match.group(2).strip()
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        label = "AI 아키텍트의 경고" if "NOTE" in type_str or "IMPORTANT" in type_str else "아키텍트 인사이트"
        return f'<div class="callout"><div class="callout-label">{label}</div><p>{content}</p></div>'

    md_text = re.sub(r'>\s*\[!(NOTE|TIP|IMPORTANT|INSIGHT)\]\s*(.*?)(?=\n\n|\n$|(?=>\s*\[!))', repl_callout, md_text, flags=re.DOTALL)

    # 2. AI Architect Card 변환 (> [!CARD 01] 제목 \n 내용)
    def repl_card(match):
        num = match.group(1)
        title = match.group(2)
        content = match.group(3).strip()
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        return f'<div class="ai-architect-card"><div class="card-number">{num}</div><div class="card-title">{title}</div><div class="card-content">{content}</div></div>'

    # 정규식 수동 보정 (복잡한 중첩 구조 대응)
    md_text = re.sub(r'>\s*\[!CARD\s*(\d+)\]\s*(.*?)\s*\n((?:>.*\n?)+)', repl_card, md_text)

    # 3. Sparkling Tip 변환
    def repl_sparkling(match):
        title = match.group(1)
        content = match.group(2).strip()
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        return f'<div class="sparkling-tip"><div class="tip-icon">💡</div><div class="tip-body"><p><strong>{title}</strong>: {content}</p></div></div>'

    md_text = re.sub(r'>\s*💡\s*\*\*\[(.*?)\]\*\*\s*(.*?)(?=\n\n|\n$)', repl_sparkling, md_text, flags=re.DOTALL)
    return md_text

path = r'C:\Obsidian_save\2026_Note\Homepage_Factory\Samantha.AI.kr\convert\chapters\3.4_형식_강제_및_데이터_무결성.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("Preprocessing...")
try:
    processed = preprocess_samantha_tags(text)
    print("Converting...")
    html = markdown.markdown(processed, extensions=['extra', 'nl2br', 'sane_lists', TocExtension()])
    print("Done!")
except Exception as e:
    import traceback
    traceback.print_exc()
