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

def make_index(base_folder_name):
    # 스크립트 실행 위치의 절대 경로 확인
    current_working_dir = os.getcwd()
    target_path = os.path.join(current_working_dir, base_folder_name)
    
    if not os.path.exists(target_path):
        print(f"❌ '{base_folder_name}' 폴더를 찾을 수 없습니다. 경로를 확인해주세요.")
        return

    # 절대 제외 목록 (보안 및 관리용)
    EXCLUDE_DIRS = ['.git', '.github', '.assets']
    EXCLUDE_FILES = ['CNAME', 'index.html', 'README.md', 'README.html']

    for root, dirs, files in os.walk(target_path):
        # 제외할 폴더가 경로에 포함되어 있으면 생략
        if any(ex in root for ex in EXCLUDE_DIRS):
            continue
        
        items_html = ""
        
        # 1. 폴더 목록 처리 (슬래시 추가)
        for d in sorted(dirs):
            if d.startswith('.') or d.endswith('.assets') or d in EXCLUDE_DIRS:
                continue
            items_html += f'<tr><td>📂 <a href="./{d}/">{d}/</a></td></tr>\n'
            
        # 2. 파일 목록 처리 (슬래시 제외)
        for f in sorted(files):
            if f.startswith('.') or f in EXCLUDE_FILES or f.endswith('.py'):
                continue
            items_html += f'<tr><td>📄 <a href="./{f}">{f}</a></td></tr>\n'
        
        # 브라우저에 표시될 상대 경로 계산 (wook413 루트 기준 가공)
        relative_path = root.replace(current_working_dir, "").replace("\\", "/")
        
        # 루트(/)인 경우 /wook413으로 표시, 그 외에는 /wook413/하위경로로 표시
        if relative_path == "" or relative_path == "/":
            display_path = "/wook413"
        else:
            # relative_path가 이미 /로 시작하므로 바로 붙여줍니다.
            display_path = "/wook413" + relative_path
        
        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html)
        
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

if __name__ == "__main__":
    # 실행 범위를 'writeups' 폴더로 제한합니다.
    make_index("writeups")
    print("✅ 'writeups' 하위 폴더들에 대한 인덱스 생성이 완료되었습니다.")