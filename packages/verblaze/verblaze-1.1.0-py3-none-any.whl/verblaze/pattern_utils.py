import json
import os

def load_patterns(template_name: str) -> dict:
    """
    Load patterns from patterns.json file for the given template
    """
    patterns_file = os.path.join(os.path.dirname(__file__), 'patterns.json')
    with open(patterns_file, 'r', encoding='utf-8') as f:
        patterns = json.load(f)
    
    return patterns.get(template_name.lower(), {}) 