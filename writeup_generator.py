import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Index of {path}</title>
    <style>
        :root {{ --bg: #ffffff; --text: #1a1a1a; --link: #0066cc; --border: #eeeeee; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); padding: 40px 20px; max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 1.5rem; border-bottom: 2px solid var(--text); padding-bottom: 10px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td {{ padding: 12px 5px; border-bottom: 1px solid var(--border); }}
        a {{ color: var(--link); text-decoration: none; }}
        a:hover {{ text-decoration: underline; background: #f0f7ff; }}
        footer {{ margin-top: 50px; font-size: 0.8rem; color: #999; text-align: center; }}
    </style>
</head>
<body>
    <h1>Index of {path}</h1>
    <table>
        <tbody>
            <tr><td><a href="../">../</a></td></tr>
            {items}
        </tbody>
    </table>
    <footer>&copy; 2026 wook413.</footer>
</body>
</html>"""

def make_index(base_dir):
    # base_dir 내부에서만 작동하도록 설정
    target_path = os.path.join(os.getcwd(), base_dir)
    
    if not os.path.exists(target_path):
        print(f"❌ '{base_dir}' 폴더를 찾을 수 없습니다.")
        return

    # 제외할 목록
    EXCLUDE_LIST = ['.git', '.github', '.assets', 'index.html']

    for root, dirs, files in os.walk(target_path):
        # 특정 제외 폴더가 경로에 포함되면 건너뜀
        if any(ex in root for ex in EXCLUDE_LIST):
            continue
        
        items_html = ""
        
        # 1. 폴더 목록 처리 (이름 뒤에 / 추가)
        for d in sorted(dirs):
            if d.startswith('.') or d.endswith('.assets') or d in EXCLUDE_LIST:
                continue
            items_html += f'<tr><td>📂 <a href="./{d}/">{d}/</a></td></tr>\n'
            
        # 2. 파일 목록 처리 (슬래시 없이 이름만)
        for f in sorted(files):
            if f.startswith('.') or f in EXCLUDE_LIST or f.endswith('.py'):
                continue
            items_html += f'<tr><td>📄 <a href="./{f}">{f}</a></td></tr>\n'
        
        # 웹 주소에 표시될 경로 계산
        # 루트(wook413) 기준의 경로를 보여주기 위해 가공
        display_path = root.replace(os.getcwd(), "").replace("\\", "/")
        
        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html)
        
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

if __name__ == "__main__":
    # 범위를 'writeups' 폴더로 한정
    make_index("writeups")
    print("✅ 'writeups' 폴더 내의 모든 인덱스 파일 생성이 완료되었습니다!")