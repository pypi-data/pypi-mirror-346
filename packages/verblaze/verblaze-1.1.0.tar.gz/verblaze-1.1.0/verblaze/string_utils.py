# string_utils.py

import re
import json
import os
import string
from termcolor import colored
from unidecode import unidecode
import asyncio
from .api import API

def remove_emojis_and_punctuation(text):
    """
    Removes emojis and punctuation from the given text.
    """
    # Define the Unicode range for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "]+", flags=re.UNICODE
    )

    # Remove punctuation
    no_punctuation = text.translate(str.maketrans("", "", string.punctuation))

    # Remove emojis
    no_emoji = emoji_pattern.sub(r'', no_punctuation)

    return no_emoji.strip()

def format_as_json(file_path_and_strings: list, secret_key:str) -> str:
    """
    Formats the extracted strings into a JSON structure.
    """
    data = []

    for file_path, strings in file_path_and_strings:
        basename = os.path.basename(file_path)
        # First characters should be uppercase, e.g., "Settings Screen"
        file_title = (basename.split(".")[0].replace("_", " ")).title()
        file_key = basename.split(".")[0]
        
        # API'yi kullanarak string'ler için key'leri oluştur
        try:
            values = asyncio.run(API.generate_keys(secret_key, strings))
            print(colored(f"Keys generated for {file_title}", "green"))
        except Exception as e:
            print(f"Error occurred while generating keys: {str(e)}")
            continue

        if values:
            data.append({"file_title": file_title, "file_key": file_key, "values": values})
            
    return json.dumps(data, ensure_ascii=False, indent=2)