import json
import os
from termcolor import colored
import sys

def process_translation_file(path, format):
    """
    Process a translation file (JSON or ARB) and return its content.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            if format == 'arb':
                # ARB metadata alanlarını temizle
                if "@@locale" in data:
                    del data["@@locale"]
                if "@@last_modified" in data:
                    del data["@@last_modified"]
                
                # @ ile başlayan tüm metadata alanlarını temizle
                data = {
                    key: value 
                    for key, value in data.items() 
                    if not key.startswith('@')
                }
            
            return data
            
    except json.JSONDecodeError:
        print(colored(f"\nInvalid {format.upper()} file format!", "red"))
        sys.exit(1)
    except Exception as e:
        print(colored(f"\nError processing file: {e}", "red"))
        sys.exit(1) 