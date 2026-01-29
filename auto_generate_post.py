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

def make_index(target_dir):
    for root, dirs, files in os.walk(target_dir):
        # .git이나 .assets 폴더 내부는 인덱스를 만들지 않음
        if '.git' in root or '.assets' in root: continue
        
        items_html = ""
        
        # 폴더 목록 (정렬 없이 그대로 추가)
        for d in dirs:
            if d.startswith('.') or d.endswith('.assets'): continue
            items_html += f'<tr><td>📂 <a href="./{d}/">{d}/</a></td></tr>\n'
            
        # 파일 목록 (정렬 없이 그대로 추가)
        for f in files:
            if f != 'index.html' and not f.endswith('.py') and not f.startswith('.'):
                items_html += f'<tr><td>📄 <a href="./{f}">{f}</a></td></tr>\n'
        
        # 경로 표시 최적화
        abs_target = os.path.abspath(target_dir)
        abs_root = os.path.abspath(root)
        display_path = abs_root.replace(abs_target, "").replace("\\", "/") or "/"
        
        full_html = HTML_TEMPLATE.format(path=display_path, items=items_html)
        
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)

if __name__ == "__main__":
    make_index(".")
    print("✅ 완료! 모든 폴더에 index.html이 생성되었습니다.")