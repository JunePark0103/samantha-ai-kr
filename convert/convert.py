#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import glob
import markdown
from pathlib import Path
from datetime import datetime
from markdown.extensions.toc import TocExtension

# ─────────────────────────────────────────────
# ★ 설정
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'books.html')
MD_FOLDER = os.path.join(BASE_DIR, 'chapters')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'html_output')
# ─────────────────────────────────────────────

def get_template():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"템플릿 파일을 찾을 수 없습니다: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def preprocess_samantha_tags(md_text):
    # 1. Callout 변환 (> [!NOTE] 등) - 내용 앞의 '>' 제거 보강
    def repl_callout(match):
        type_str = match.group(1).upper()
        content = match.group(2).strip()
        # 내용 내의 모든 줄에서 시작하는 '>' 제거
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        
        label = "AI 아키텍트의 경고" if "NOTE" in type_str or "IMPORTANT" in type_str else "아키텍트 인사이트"
        style = ""
        label_style = ""
        if "TIP" in type_str or "INSIGHT" in type_str:
            style = 'style="background: var(--teal-dim); border-color: var(--teal-border); border-left-color: var(--teal);"'
            label_style = 'style="color: var(--teal);"'
        return f'<div class="callout" {style}><div class="callout-label" {label_style}>{label}</div><p>{content}</p></div>'

    md_text = re.sub(r'>\s*\[!(NOTE|TIP|IMPORTANT|INSIGHT)\]\s*(.*?)(?=\n\n|\n$|(?=>\s*\[!))', repl_callout, md_text, flags=re.DOTALL)

    # 2. AI Architect Card 변환 (> [!CARD 01] 제목 \n 내용)
    def repl_card(match):
        num = match.group(1)
        title = match.group(2)
        content = match.group(3).strip()
        # 내용 내의 모든 줄에서 시작하는 '>' 제거
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        return f'<div class="ai-architect-card"><div class="card-number">{num}</div><div class="card-title">{title}</div><div class="card-content">{content}</div></div>'

    # 정규식 수동 보정 (복잡한 중첩 구조 대응)
    md_text = re.sub(r'>\s*\[!CARD\s*(\d+)\]\s*(.*?)\s*\n((?:>.*\n?)+)', repl_card, md_text)

    # 3. Sparkling Tip 변환
    def repl_sparkling(match):
        title = match.group(1)
        content = match.group(2).strip()
        # 내용 내의 모든 줄에서 시작하는 '>' 제거
        content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
        return f'<div class="sparkling-tip"><div class="tip-icon">💡</div><div class="tip-body"><p><strong>{title}</strong>: {content}</p></div></div>'

    md_text = re.sub(r'>\s*💡\s*\*\*\[(.*?)\]\*\*\s*(.*?)(?=\n\n|\n$)', repl_sparkling, md_text, flags=re.DOTALL)

    return md_text

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    template = get_template()
    md_files = sorted(glob.glob(os.path.join(MD_FOLDER, "*.md")))

    if not md_files:
        print("변환할 마크다운 파일이 없습니다.")
        return

    # 메인 컨텐츠 영역 정규식
    main_pattern = re.compile(r'(<main class="chapter-content">)(.*?)(</main>)', re.DOTALL)

    # 7. 내비게이션 (이전/다음) 생성
    chapters_info = []
    for f in md_files:
        fname = os.path.basename(f)
        ch_m = re.match(r'(\d+\.\d+)', fname)
        c_num = ch_m.group(1) if ch_m else "0.0"
        
        # 파일 내부에서 제목 추출 시도
        with open(f, 'r', encoding='utf-8') as tf:
            first_line = tf.readline()
            c_title = first_line.replace('# ', '').strip() if first_line.startswith('# ') else fname.replace('.md', '')
        
        chapters_info.append({'file': fname.replace('.md', '.html'), 'num': c_num, 'title': c_title})

    for idx, md_path in enumerate(md_files):
        filename = os.path.basename(md_path)
        print(f"변환 중: {filename}...")
        
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                raw_md = f.read()

            # 전처리
            processed_md = preprocess_samantha_tags(raw_md)
            
            # 제목 추출
            lines = processed_md.split('\n')
            title = filename.replace('.md', '')
            if lines and lines[0].startswith('# '):
                title = lines[0].replace('# ', '').strip()
                processed_md = '\n'.join(lines[1:])

            # 마크다운 변환
            extensions = ['extra', 'nl2br', 'sane_lists', TocExtension(slugify=lambda x,y: x.lower().replace(' ', '-'))]
            body_html = markdown.markdown(processed_md, extensions=extensions)

            # 챕터 번호 추출
            ch_num = chapters_info[idx]['num']

            # 1) 내비게이션 버튼 생성 (Fallback 포함)
            prev_link = f'<a href="../../books.html" class="ch-nav-btn"><div class="nav-label">← LIBRARY</div><div class="nav-title">목차로 돌아가기</div></a>'
            next_link = f'<a href="../../join.html" class="ch-nav-btn next"><div class="nav-label">JOIN →</div><div class="nav-title">새 소식 받기</div></a>'
            
            if idx > 0:
                p = chapters_info[idx-1]
                prev_link = f'<a href="{p["file"]}" class="ch-nav-btn"><div class="nav-label">← PREV</div><div class="nav-title">{p["num"]} {p["title"]}</div></a>'
            
            if idx < len(chapters_info) - 1:
                n = chapters_info[idx+1]
                next_link = f'<a href="{n["file"]}" class="ch-nav-btn next"><div class="nav-label">NEXT →</div><div class="nav-title">{n["num"]} {n["title"]}</div></a>'
            
            nav_html = f'<div class="ch-nav">{prev_link}{next_link}</div>'

            # 2) 사이드바 TOC active 클래스 및 open 속성 부여
            # books.html의 아코디언 구조를 그대로 유지하면서, 현재 챕터만 active/open 처리
            target_href = f'convert/html_output/{filename.replace(".md", ".html")}'

            # 3) 전체 컨텐츠 조립 및 주입
            injected_content = f"""
        <article class="chapter-section active">
          <div class="ch-eyebrow">CHAPTER {ch_num} · OPEN EDITION</div>
          <h1 class="ch-title">{title}</h1>
          <div class="ch-body">
            {body_html}
          </div>
        </article>
        {nav_html}
    """
            
            # 메인 컨텐츠 주입
            final_html = main_pattern.sub(lambda m: m.group(1) + injected_content + m.group(3), template)
            
            # TOC active 주입 및 details open 상태 변경
            final_html = final_html.replace(
                f'href="{target_href}" class="toc-sub-item"',
                f'href="{target_href}" class="toc-sub-item active"'
            )
            final_html = final_html.replace('class="toc-details toc-group" open', 'class="toc-details toc-group"')
            
            def open_active_details(match):
                content = match.group(0)
                if 'active' in content:
                    return content.replace('class="toc-details toc-group"', 'class="toc-details toc-group" open')
                return content
                
            final_html = re.sub(r'<details class="toc-details toc-group">.*?</details>', open_active_details, final_html, flags=re.DOTALL)

            # 4) 경로 자동 수정 (더 견고한 정규식)
            # TOC 내의 내부 챕터 링크는 동일 폴더 내이므로 상대경로 제거
            final_html = final_html.replace('href="convert/html_output/', 'href="./')
            # 그 외 루트 레벨 에셋들은 ../../ 를 붙여서 참조하도록 보정
            final_html = re.sub(r'(href|src)="(?!http|\.\./|\./|#)([^"]+)"', r'\1="../../\2"', final_html)

            # 5) 진행률 자동 주입
            # idx=0이 첫 챕터, idx=len-1이 마지마 장
            progress_pct = round(((idx + 1) / len(chapters_info)) * 100)
            progress_label = f"CH {ch_num} 읽는 중"

            final_html = re.sub(
                r'id="progress-fill"[^>]*style="width:[^"]*"',
                f'id="progress-fill" style="width: {progress_pct}%;"',
                final_html
            )
            final_html = re.sub(
                r'(<span id="progress-percent">)[^<]*(</span>)',
                rf'\g<1>{progress_pct}%\g<2>',
                final_html
            )
            final_html = re.sub(
                r'(<span id="progress-text">)[^<]*(</span>)',
                rf'\g<1>{progress_label}\g<2>',
                final_html
            )

            # 저장
            output_path = os.path.join(OUTPUT_FOLDER, filename.replace('.md', '.html'))
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
        except Exception as e:
            print(f"[ERROR] {filename} 변환 중 오류 발생!")
            import traceback
            traceback.print_exc()
            return

    print(f"\n[SUCCESS] 총 {len(md_files)}개의 파일이 변환되었습니다.")

if __name__ == "__main__":
    main()
