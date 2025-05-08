# file_utils.py

import os

def get_actual_path(template: str):
    """
    Returns the actual path within the project where the code resides,
    based on the technology/template used.
    """
    actual_paths = {
        "flutter": "lib",
        "react": "",
        "react-native": "",
        "angular": "src/app",
        "plain-html": "",
        "vue": "src",
        "svelte": "src",
        "ember": "app",
        "backbone": "src",
        "swift": "",
        "kotlin": "",
        "javafx": "src",
        "wpf": "src",
        "qt": "src",
        "blazor": "Pages",
        "nextjs": "",
    }
    return actual_paths.get(template, "")

def get_file_extension_from_template(template: str):
    """
    Returns the file extensions associated with the given template.
    """
    extensions = {
        "flutter": ("dart",),
        "react": ("jsx", "tsx", "js", "ts"),
        "react-native": ("jsx", "tsx", "js", "ts"),
        "angular": ("ts", "html"),
        "plain-html": ("html",),
        "vue": ("vue",),
        "svelte": ("svelte",),
        "ember": ("js", "hbs"),
        "backbone": ("js",),
        "swift": ("swift", "storyboard", "xib"),
        "kotlin": ("kt", "xml"),
        "javafx": ("java", "fxml"),
        "wpf": ("xaml",),
        "qt": ("qml",),
        "blazor": ("razor",),
        "nextjs": ("jsx", "tsx", "js", "ts"),
    }
    return extensions.get(template, ())

def list_all_files_in_directory(dir_path: str, template: str, folders: list):
    """
    Lists all files in the given directory and its subdirectories that match the specified
    template and are located within the specified folders.
    """
    valid_file_extensions = get_file_extension_from_template(template)
    if not valid_file_extensions:
        raise ValueError(f"No file extensions found for template: {template}")
    all_files = []

    for root, dirs, files in os.walk(dir_path):
        current_folder = os.path.basename(root)
        parent_folder = os.path.basename(os.path.dirname(root))

        # Ana dizindeki dosyaları veya belirtilen klasörlerdeki dosyaları kontrol et
        if current_folder in folders or parent_folder in folders or root == dir_path:
            for file in files:
                if file.endswith(tuple(f".{ext}" for ext in valid_file_extensions)):
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
    return all_files