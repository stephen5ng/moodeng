#!/usr/bin/env python3
import csv
import os
import re

def read_clues_from_csv(filename):
    """Read clues from a CSV file, extracting the second field from each line."""
    try:
        clues = []
        codes = []
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Strip quotes and whitespace from the second field
                clue = row[1].strip().strip('"').strip("'")
                clues.append(clue)
        return codes, clues
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

def replace_clues_in_template(template_content, clues):
    """Replace the clues array in the template with the new clues and generate static HTML for the button and clues."""
    # Find the line with the clues array
    lines = template_content.split('\n')
    
    for i, line in enumerate(lines):
        if "var clues = ['REPLACE_CLUES_HERE'];" in line:
            # Replace the clues array
            new_clues_array = generate_clues_array(clues)
            lines[i] = f"    var clues = {new_clues_array};"
            break
    
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
    os.makedirs('generated_html', exist_ok=True)
    
    template_content = read_template_file('template.buttons.html')
    if template_content is None:
        return
    
    clues_dir = 'clues'
    if not os.path.exists(clues_dir):
        print(f"Error: Directory '{clues_dir}' not found.")
        return
    
    for filename in os.listdir(clues_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(clues_dir, filename)
            print(f"\nProcessing {input_file}...")
            
            codes, clues = read_clues_from_csv(input_file)            
            print(f"Loaded {len(clues)} clues from {filename}")

            modified_template = replace_clues_in_template(template_content, clues)

            basename = os.path.splitext(filename)[0]
            output_html = f"generated_html/{basename}.html"

            write_html_file(output_html, modified_template)
                
    print(f"\nCompleted processing all files in {clues_dir}/")

if __name__ == "__main__":
    main()