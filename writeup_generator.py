import os
import sys

from site_common import HOME_CSS

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <title>wook413</title>
    <style>
        :root {{ --bg: #fdfbf7; --text: #262220; --muted: #7a736a; --link: #0f5fae; --border: #e7e1d6; --row-hover: #eef3f8; }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: "Nunito", "Apple SD Gothic Neo", "Malgun Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: var(--bg); color: var(--text); padding: 56px 20px 80px; max-width: 760px; margin: 0 auto; line-height: 1.6; }}
        h1 {{ font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid var(--text); padding-bottom: 14px; margin: 0 0 28px; word-break: break-all; }}
        table {{ width: 100%; border-collapse: collapse; }}

        td {{ border-bottom: 1px solid var(--border); padding: 0; }}
        td a {{
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--link);
            text-decoration: none;
            padding: 12px 10px;
            border-radius: 6px;
            margin: 0 -10px;
        }}

        td a span.label {{
            border-radius: 3px;
        }}

        td a:hover {{
            background: var(--row-hover);
        }}

        td a:hover span.label {{
            text-decoration: underline;
        }}

        footer {{ margin-top: 20px; font-size: 0.8rem; color: var(--muted); text-align: center; }}
        @media (max-width: 600px) {{ body {{ padding: 32px 16px 60px; }} h1 {{ font-size: 1.15rem; }} }}
    </style>
    <style>{home_css}</style>
</head>
<body>
    {home_link}
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

        depth = relative_path.strip("/").count("/") + 1
        home_link = f'<a class="home-link" href="{"../" * depth}index.html">🏠 Home</a>'

        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html, home_css=HOME_CSS, home_link=home_link)
        
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

if __name__ == "__main__":
    # 이제 처리하고 싶은 상위 폴더들만 리스트로 넣어주면 끝!
    folders = ["writeups"]
    for folder in folders:
        make_index(folder)
    print("✅ 모든 인덱스 생성이 완료되었습니다!")