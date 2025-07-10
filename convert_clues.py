import csv

def convert_csv_to_js():
    clues = {}
    
    with open('clues.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                hider_id = row[0][0]  # First character of first field
                clue = row[1]         # Second field
                if hider_id not in clues:
                    clues[hider_id] = []
                clues[hider_id].append(clue)
    
    # Write to JavaScript file
    with open('clues.js', 'w') as jsfile:
        jsfile.write('var clues = {\n')
        for hider_id, clue_list in clues.items():
            jsfile.write(f'    "{hider_id}": {clue_list},\n')
        jsfile.write('};\n')

if __name__ == "__main__":
    convert_csv_to_js()
    print("Converted clues.csv to clues.js") 