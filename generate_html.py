#!/usr/bin/env python3
import csv
import os

HIDER_COLORS = {
    "S": "TURQUOISE",
    "G": "PINK"
}

def read_clues_from_csv(filename):
    """Read clues from a CSV file, extracting the second field from each line."""
    try:
        clues = []
        codes = []
        hider_code = None
        last_hider_code = None
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print(row)
                if len(row) < 2:
                    continue
                clue = row[1].strip().strip('"').strip("'")
                hider_code = clue[0]
                clues.append(clue)
                codes.append(row[0].strip().strip('"').strip("'"))
            if last_hider_code and hider_code != last_hider_code:
                yield codes, clues
                codes = []
                clues = []
        print(f"Loaded {len(codes)} codes and {len(clues)} clues from {filename}")
        yield codes, clues
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def read_template_file(filename):
    """Read the HTML template file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading template: {e}")
        return None

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
    """Replace the clues array in the template with the new clues and generate static HTML for the button and clues."""
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
    """Write the generated HTML content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully generated '{filename}'")
    except Exception as e:
        print(f"Error writing file: {e}")

def main():    
    template_buttons_content = read_template_file('template.buttons.html')
    template_single_content = read_template_file('template.single.html')
    template_cookie_content = read_template_file('template.cookie.html')
    
    filename = "clues.csv"
    print(f"\nProcessing {filename}...")

    for codes, clues in read_clues_from_csv(filename):
        print(f"Loaded {len(clues)} clues from {filename}")

        for code, clue in zip(codes, clues):
            modified_template = replace_clues_in_template(
                template_single_content, clues, clue, HIDER_COLORS[code[0]])
            os.makedirs(f"generated_html/single/{code}", exist_ok=True)
            output_html = f"generated_html/single/{code}/index.html"
            write_html_file(output_html, modified_template)
        
        basename = os.path.splitext(filename)[0]
        write_html_file(f"generated_html/buttons/{basename}.html", modified_template)
        for code, clue in zip(codes, clues):
            modified_template = replace_clues_in_template(
                template_buttons_content, clues, clue, HIDER_COLORS[code[0]])
            os.makedirs(f"generated_html/buttons/{code}", exist_ok=True)
            output_html = f"generated_html/buttons/{code}/index.html"
            write_html_file(output_html, modified_template)

        for code, clue in zip(codes, clues):
            modified_cookie_template = replace_clues_in_template(
                template_cookie_content, clues, clue, HIDER_COLORS[code[0]])
            os.makedirs(f"generated_html/cookie/{code}", exist_ok=True)
            output_html = f"generated_html/cookie/{code}/index.html"
            write_html_file(output_html, modified_cookie_template)

if __name__ == "__main__":
    main()