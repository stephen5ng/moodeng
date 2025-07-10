#!/usr/bin/env python3
import csv
import os

HIDER_COLORS = {
    "S": "TURQUOISE",
    "G": "PINK"
}

def read_clues_from_csv(filename):
    clues = []
    codes = []
    hider_code = None
    last_hider_code = None
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, quotechar='"')
        for row in csv_reader:
            if len(row) < 2:
                continue
            code, clue = row
            hider_code = code[0]
            if last_hider_code and hider_code != last_hider_code:
                print(f"yielding {codes}, {clues}")
                yield codes, clues
                codes = []
                clues = []
            last_hider_code = hider_code

            codes.append(code)
            clues.append(clue)
            print(f"codes: {hider_code}, {last_hider_code}")
    print(f"Loaded {len(codes)} codes and {len(clues)} clues from {filename}")
    yield codes, clues

def read_template_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def generate_clues_array(clues):
    """Generate JavaScript array string from clues list."""
    if not clues:
        return "[]"

    # Escape quotes and format as JavaScript array
    escaped_clues = []
    for clue in clues:
        # Escape single quotes and backslashes for JavaScript
        escaped_clue = clue.replace("\\", "\\\\").replace("'", "\\'")
        escaped_clues.append(f"'{escaped_clue}'")

    return "[" + ",\n".join(escaped_clues) + "]"

def replace_clues_in_template(template_content, clues, clue, hider_color):
    """Replace the template strings."""
    lines = template_content.split('\n')
    
    for i, line in enumerate(lines):
        if "REPLACE_CLUES_HERE" in line:
            new_clues_array = generate_clues_array(clues)
            lines[i] = line.replace(
                "REPLACE_CLUES_HERE", new_clues_array
            )
        elif "REPLACE_CLUE_HERE" in line:
            lines[i] = line.replace("REPLACE_CLUE_HERE", clue)
        elif "REPLACE_COLOR_HERE" in line:
            lines[i] = line.replace("REPLACE_COLOR_HERE", hider_color)
    
    return '\n'.join(lines)

def write_html_file(filename, content):
    print(f"filename: {filename}")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main():    
    template_single_content = read_template_file('template.single.html')
    template_cookie_content = read_template_file('template.cookie.html')
    
    filename = "clues.csv"
    print(f"\nProcessing {filename}...")

    for codes, clues in read_clues_from_csv(filename):
        print(f"Loaded {len(clues)} clues from {filename}")
        for template, subdir in (
            (template_single_content, "single"),
            (template_cookie_content, "cookie")):
            for code, clue in zip(codes, clues):
                modified_template = replace_clues_in_template(
                    template, clues, clue, HIDER_COLORS[code[0]])
                os.makedirs(f"generated_html/{subdir}/{code}", exist_ok=True)
                output_html = f"generated_html/{subdir}/{code}/index.html"
                write_html_file(output_html, modified_template)

if __name__ == "__main__":
    main()