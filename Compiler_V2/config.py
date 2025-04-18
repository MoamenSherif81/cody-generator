import json
import re
from typing import Dict, Tuple


def load_config(file_path: str) -> Tuple[Dict[str, Dict], str, str]:
    """Load configuration from JSON file."""
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {file_path}")

    tag_mappings = config.get("tagMappings", {})
    opening_tag = config.get("openingTag", "{")
    closing_tag = config.get("closingTag", "}")

    processed_mappings = {}

    for tag, settings in tag_mappings.items():
        # Handle new format
        html_tag = settings.get("htmlTag")
        css_classes = settings.get("cssClasses", [])
        css_attributes = settings.get("cssAttributes", {})
        text_limit = settings.get("textLimit", 0)
        default_color = settings.get("defaultColor", [0, 0, 0])

        # Handle legacy format (htmlTag as template, e.g., "<div class='row'>[]</div>")
        if not html_tag:
            template = settings.get("htmlTag", "")
            tag_match = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)', template)
            html_tag = tag_match.group(1) if tag_match else ""
            class_match = re.search(r"class='([^']*)'", template)
            css_classes = class_match.group(1).split() if class_match else []

        # Ensure css_classes is a list
        if isinstance(css_classes, str):
            css_classes = css_classes.split()
        elif not isinstance(css_classes, list):
            css_classes = []

        # Validate default-color
        if not isinstance(default_color, list) or len(default_color) != 3 or not all(
                isinstance(x, int) and 0 <= x <= 255 for x in default_color):
            default_color = [0, 0, 0]

        processed_mappings[tag] = {
            "htmlTag": html_tag,
            "cssClasses": css_classes,
            "cssAttributes": css_attributes,
            "textLimit": text_limit,
            "defaultColor": tuple(default_color)
        }

    return processed_mappings, opening_tag, closing_tag
