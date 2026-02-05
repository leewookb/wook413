import os

# 1. HTML 템플릿
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
        body {{ font-family: -apple-system, 'JetBrains Mono', 'Roboto Mono', 'Consolas', monospace; background: var(--bg); color: var(--text); padding: 40px 20px; max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 1.5rem; border-bottom: 2px solid var(--text); padding-bottom: 10px; margin-bottom: 20px; word-break: break-all; }}
        table {{ width: 100%; border-collapse: collapse; }}
        
        td {{ border-bottom: 1px solid var(--border); padding: 10px 5px; }}
        td a {{ 
            display: inline-flex; 
            align-items: center; 
            gap: 8px; 
            color: var(--link); 
            text-decoration: none; 
        }}
        
        td a span.label {{ 
            padding: 2px 4px; 
            border-radius: 3px; 
            transition: background 0.2s;
        }}
        
        td a:hover span.label {{ 
            text-decoration: underline; 
            background: #f0f7ff; 
        }}

        footer {{ margin-top: 50px; font-size: 0.8rem; color: #999; text-align: center; }}
        @media (max-width: 600px) {{ body {{ padding: 15px; }} h1 {{ font-size: 1.1rem; }} }}
    </style>
</head>
<body>
    <h1>Index of {path}</h1>
    <table>
        <tbody>
            <tr><td><a href="../"><span>⤴️</span> <span class="label">../</span></a></td></tr>
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

    EXCLUDE_DIRS = ['.git', '.github', '.assets', 'OSCP']
    EXCLUDE_FILES = ['CNAME', 'index.html', 'README.md', 'README.html']

    for root, dirs, files in os.walk(target_path):
        if any(ex in root for ex in EXCLUDE_DIRS):
            continue
        
        items_list = []
        
        # 폴더 목록 생성
        for d in sorted(dirs):
            if d.startswith('.') or d.endswith('.assets') or d in EXCLUDE_DIRS:
                continue
            items_list.append(f'<tr><td><a href="./{d}/"><span>📂</span> <span class="label">{d}/</span></a></td></tr>')
            
        # 파일 목록 생성
        for f in sorted(files):
            if f.startswith('.') or f in EXCLUDE_FILES or f.endswith('.py'):
                continue
            
            # 확장자에 따라 아이콘 분류
            icon = "📄"
            if f.lower().endswith(('.svg', '.png', '.jpg', '.jpeg', '.gif')):
                icon = "🖼️"
            elif f.lower().endswith('.pdf'):
                icon = "📕"
            
            items_list.append(f'<tr><td><a href="./{f}"><span>{icon}</span> <span class="label">{f}</span></a></td></tr>')
        
        items_html = "\n".join(items_list)
        
        relative_path = root.replace(current_working_dir, "").replace("\\", "/")
        display_path = "/wook413" + (relative_path if relative_path not in ["", "/"] else "")
        
        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html)
        
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

if __name__ == "__main__":
    # 이제 처리하고 싶은 상위 폴더들만 리스트로 넣어주면 끝!
    folders = ["writeups"]
    for folder in folders:
        make_index(folder)
    print("✅ 모든 인덱스 생성이 완료되었습니다!")