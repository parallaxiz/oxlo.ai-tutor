import os

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_html = False
current_html_lines = []
current_var_name = ""
os.makedirs("ui", exist_ok=True)

for line in lines:
    if not in_html and ('_HTML = """<!DOCTYPE html>' in line or '_HTML = """' in line):
        current_var_name = line.strip().split(' = ')[0]
        in_html = True
        html_start = line.split('"""', 1)[1]
        if html_start:
            current_html_lines.append(html_start)
    elif in_html:
        if '</html>"""' in line:
            html_end = line.split('"""', 1)[0]
            current_html_lines.append(html_end + '\n')
            filename = current_var_name.lower().replace('_html', '.html')
            with open(os.path.join("ui", filename), "w", encoding="utf-8") as out:
                out.write("".join(current_html_lines))
            in_html = False
            current_html_lines = []
            current_var_name = ""
        else:
            current_html_lines.append(line)
        
print("SUCCESS - Files extracted cleanly.")
