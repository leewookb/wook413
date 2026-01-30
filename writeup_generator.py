import os

# 1. HTML 템플릿 (CSS 정렬 및 모바일 최적화 보강)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="/assets/favicon_io/site.webmanifest">
    <title>wook413</title>
    <style>
        :root {{ --bg: #ffffff; --text: #1a1a1a; --link: #0066cc; --border: #eeeeee; }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); padding: 40px 20px; max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 1.5rem; border-bottom: 2px solid var(--text); padding-bottom: 10px; margin-bottom: 20px; word-break: break-all; }}
        table {{ width: 100%; border-collapse: collapse; }}
        
        /* 아이콘과 텍스트가 한 줄에 나오도록 Flexbox 적용 */
        td {{ border-bottom: 1px solid var(--border); }}
        td a {{ 
            display: flex; 
            align-items: center; 
            gap: 10px; 
            padding: 12px 5px; 
            color: var(--link); 
            text-decoration: none; 
        }}
        td a:hover {{ text-decoration: underline; background: #f0f7ff; }}
        
        footer {{ margin-top: 50px; font-size: 0.8rem; color: #999; text-align: center; }}
        @media (max-width: 600px) {{ body {{ padding: 15px; }} h1 {{ font-size: 1.1rem; }} }}
    </style>
</head>
<body>
    <h1>Index of {path}</h1>
    <table>
        <tbody>
            <tr><td><a href="../">⤴️ ../</a></td></tr>
            {items}
        </tbody>
    </table>
    <footer>&copy; 2026 wook413.</footer>
</body>
</html>"""

def make_index(base_folder_name):
    current_working_dir = os.getcwd()
    target_path = os.path.join(current_working_dir, base_folder_name)
    
    if not os.path.exists(target_path):
        print(f"❌ '{base_folder_name}' 폴더를 찾을 수 없습니다.")
        return

    EXCLUDE_DIRS = ['.git', '.github', '.assets']
    EXCLUDE_FILES = ['CNAME', 'index.html', 'README.md', 'README.html']

    for root, dirs, files in os.walk(target_path):
        if any(ex in root for ex in EXCLUDE_DIRS):
            continue
        
        items_html = ""
        
        # 폴더 목록 생성
        for d in sorted(dirs):
            if d.startswith('.') or d.endswith('.assets') or d in EXCLUDE_DIRS:
                continue
            items_html += f'<tr><td><a href="./{d}/">📂 {d}/</a></td></tr>\n'
            
        # 파일 목록 생성
        for f in sorted(files):
            if f.startswith('.') or f in EXCLUDE_FILES or f.endswith('.py'):
                continue
            items_html += f'<tr><td><a href="./{f}">📄 {f}</a></td></tr>\n'
        
        # 경로 표시용 문자열 생성
        relative_path = root.replace(current_working_dir, "").replace("\\", "/")
        display_path = "/wook413" + (relative_path if relative_path not in ["", "/"] else "")
        
        # HTML 내용 완성
        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html)
        
        # 2. 파일 저장 로직 (이 부분이 추가되었습니다)
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

# 3. 메인 실행부 및 완료 메시지
if __name__ == "__main__":
    folder_to_process = "writeups"
    make_index(folder_to_process)
    print(f"✅ '{folder_to_process}' 하위 폴더들에 인덱스 생성이 완료되었습니다.")