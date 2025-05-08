# string_extractors.py

import re
import string
from .pattern_utils import load_patterns

class BaseStringExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.patterns = load_patterns(self.__class__.__name__.replace('StringExtractor', '').lower())

    def extract_strings(self):
        raise NotImplementedError("This method should be implemented in the subclass.")

    def remove_emojis_and_punctuation(self, text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+", flags=re.UNICODE
        )
        no_punctuation = text.translate(str.maketrans("", "", string.punctuation))
        no_emoji = emoji_pattern.sub(r'', no_punctuation)
        return no_emoji.strip()

    def filter_strings(self, strings):
        """Basic filtering based on prefixes_to_ignore list"""
        prefixes_to_ignore = self.patterns.get('prefixes_to_ignore', [])
        unique_strings = set()
        for s in strings:
            s = s.strip()
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)
        return list(unique_strings)
        
    def is_valid_string_for_translation(self, string):
        """Checks if a string is valid for translation"""
        s = string.strip()
        
        # Ignore empty or too short strings
        if len(s) < 2:
            return False
            
        # Ignore file paths, URLs, or extensions
        if re.match(r'^[./\\]', s) or re.search(r'\.(png|jpg|jpeg|gif|svg|pdf|ttf|mp3|mp4|html|js|css)$', s, re.IGNORECASE):
            return False
            
        # Ignore strings that are just numbers
        if re.match(r'^\d+(\.\d+)?$', s):
            return False
            
        # Ignore hex values (like colors)
        if re.match(r'^#[0-9a-fA-F]{3,8}$', s):
            return False
            
        # Ignore code identifiers
        if re.match(r'^[a-z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)+$', s) or re.match(r'^[a-z][a-z0-9]*(_[a-z0-9]+)+$', s):
            return False
            
        return True
        
    def has_natural_language_characteristics(self, string):
        """Checks if the text shows natural language characteristics"""
        s = string.strip()
        
        # Natural language usually contains spaces
        if ' ' in s:
            return True
            
        # Natural language usually contains punctuation
        if any(p in s for p in '.,:;!?'):
            return True
            
        # Sentences that start with uppercase and continue with lowercase may be natural language
        if len(s) > 1 and s[0].isupper() and s[1:].islower():
            return True
            
        return False
        
    def advanced_filtering(self, strings, additional_patterns=None, keywords=None):
        """Common method for advanced filtering"""
        filtered_strings = []
        
        # If additional patterns and keywords are not specified
        if additional_patterns is None:
            additional_patterns = self.patterns.get('filtering_patterns', [])
            
        if keywords is None:
            keywords = self.patterns.get('keywords_to_ignore', [])
        
        for s in strings:
            s = s.strip()
            
            # Skip empty strings
            if not s:
                continue
                
            # Filter according to additional patterns
            if additional_patterns and any(re.search(pattern, s) for pattern in additional_patterns):
                continue
                
            # Filter according to keywords
            if keywords and s in keywords:
                continue
            
            # Add strings that have natural language characteristics and are suitable for translation
            if self.has_natural_language_characteristics(s) and self.is_valid_string_for_translation(s):
                filtered_strings.append(s)
                
        return filtered_strings

EXTRACTOR_REGISTRY = {}

def register_extractor(template_name):
    def decorator(cls):
        EXTRACTOR_REGISTRY[template_name.lower()] = cls
        return cls
    return decorator

@register_extractor("flutter")
class FlutterStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] for m in matches if m[0] or m[1]])
                else:
                    strings.extend(matches)

        return self.filter_strings(strings)

@register_extractor("react")
@register_extractor("react-native")
@register_extractor("nextjs")
class ReactStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        # JSX patterns
        for pattern in self.patterns.get('jsx_patterns', []):
            matches = re.findall(pattern['pattern'], code, re.VERBOSE)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] for m in matches if m[0] or m[1]])
                else:
                    strings.extend(matches)

        # Template literals
        for pattern in self.patterns.get('template_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            for match in matches:
                clean_match = re.sub(r"\${[^}]+}", "", match).strip()
                if clean_match:
                    strings.append(clean_match)

        return self.filter_strings(strings)

@register_extractor("swift")
class SwiftStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        ui_strings = []  # Strings from UI components (like Text)
        
        if self.file_path.endswith(('.storyboard', '.xib')):
            for pattern in self.patterns.get('ui_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)
        else:
            for pattern in self.patterns.get('code_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                
                # Special handling for UI component texts like Text()
                if pattern.get('name') in ['text_component']:
                    ui_strings.extend(matches)
                else:
                    strings.extend(matches)

        # Basic filtering
        filtered_strings = self.filter_strings(strings)
        
        # Add UI strings (these are usually texts that need translation)
        filtered_strings.extend(ui_strings)
        
        # Swift-specific advanced filtering
        return self.advanced_filtering(filtered_strings)

@register_extractor("kotlin")
class KotlinStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        ui_strings = []  # Strings from UI components (Text, Button, etc.)
        
        # Check if this is an XML file (layout, menu, etc.)
        if self.file_path.endswith('.xml'):
            for pattern in self.patterns.get('ui_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)
        else:
            # This is a Kotlin/Java file
            for pattern in self.patterns.get('code_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                
                # Special handling for Jetpack Compose UI components
                if pattern.get('name') in ['text_component', 'text_component_res', 'button_component', 
                                          'alertdialog_component', 'alertdialog_message']:
                    ui_strings.extend(matches)
                else:
                    strings.extend(matches)

        # Basic filtering for regular strings
        filtered_strings = self.filter_strings(strings)
        
        # Add UI strings directly (these are usually text that needs translation)
        filtered_strings.extend(ui_strings)
        
        # Apply advanced filtering
        return self.advanced_filtering(filtered_strings)

@register_extractor("blazor")
class BlazorStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] or m[2] for m in matches if m[0] or m[1] or m[2]])
                else:
                    strings.extend(matches)

        for pattern in self.patterns.get('template_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            for match in matches:
                clean_match = re.sub(r"\${[^}]+}", "", match).strip()
                if clean_match:
                    strings.append(clean_match)

        filtered_strings = self.filter_strings(strings)
        return self.advanced_filtering(filtered_strings)

@register_extractor("qt")
class QtStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            strings.extend(matches)

        filtered_strings = self.filter_strings(strings)
        return self.advanced_filtering(filtered_strings)

def get_string_extractor(template, file_path):
    extractor_class = EXTRACTOR_REGISTRY.get(template.lower())
    if extractor_class:
        return extractor_class(file_path)
    else:
        raise ValueError(f"Unsupported template type: {template}")