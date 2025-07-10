#!/usr/bin/env python3

import csv

def convert_csv_to_js():
    clues = {}
    codes = {}
    
    with open('clues.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                code = row[0]
                clue = row[1]
                hider_id = code[0]
                
                if hider_id not in clues:
                    clues[hider_id] = []
                clues[hider_id].append(clue)
                
                codes[code] = clue
    
    with open('clues.js', 'w') as jsfile:
        jsfile.write('var clues = {\n')
        for hider_id, clue_list in clues.items():
            jsfile.write(f'    "{hider_id}": {clue_list},\n')
        jsfile.write('};\n\n')
        
        jsfile.write('var codes = {\n')
        for code, clue in codes.items():
            jsfile.write(f'    "{code}": true,\n')
        jsfile.write('};\n')

if __name__ == "__main__":
    convert_csv_to_js()
    print("Converted clues.csv to clues.js") 