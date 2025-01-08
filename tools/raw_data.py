import requests
import json
from typing import Any, Dict, List, Union, Optional

def compress_json(json_data, max_array_length=2, max_string_length=50, indent=2):
    import json
    
    def compress_string(s):
        if not isinstance(s, str):
            return s
        if len(s) <= max_string_length:
            return s
        return f"{s[:max_string_length]}... ({len(s) - max_string_length} more chars)"
    
    def process_value(value):
        if isinstance(value, list):
            if not value:
                return []
            
            if len(value) > max_array_length:
                compressed = value[:max_array_length]
                compressed.append(f"... ({len(value) - max_array_length} more items)")
                return [process_value(item) for item in compressed]
            return [process_value(item) for item in value]
            
        elif isinstance(value, dict):
            return {k: process_value(v) for k, v in value.items()}
        
        elif isinstance(value, str):
            return compress_string(value)
            
        return value

    compressed_data = process_value(json_data)
    return json.dumps(compressed_data, indent=indent)
try:
    with open("doc2.md", "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        indentation = len(line) - len(line.lstrip())
        indent_str = ' ' * indentation
        
        words = line.split(' ')
        modified_line = []
        json_block = None
        
        for w in words:
            if w.startswith("https://jsonhero.io"):
                try:
                    x = requests.get(w+".json")
                    custom_sample = compress_json(x.json())
                    json_block = [
                        '',  
                        indent_str + '```json',
                        *[indent_str + line for line in custom_sample.split('\n')],
                        indent_str + '```'
                    ]
                except Exception as e:
                    print(f"Error processing URL {w}: {e}")
                    modified_line.append(w)
            else:
                modified_line.append(w)
        
        modified_line = ' '.join(modified_line).rstrip()
        if modified_line:
            new_lines.append(modified_line)
            
        if json_block:
            new_lines.extend(json_block)
        
        i += 1
    
    with open("doc2_edited.md", "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))

except FileNotFoundError:
    print("Error: doc1.md file not found")
except UnicodeDecodeError as ude:
    print(f"Error decoding file: {ude}")
except Exception as e:
    print(f"Error reading file: {e}")