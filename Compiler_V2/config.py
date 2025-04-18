import json
from typing import Tuple, Dict


def load_config(json_file: str) -> Tuple[Dict[str, str], Dict[str, int], Dict[str, Tuple[int, int, int]], str, str]:
    """Load tag mappings, text limits, default colors, and special characters from JSON file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Extract special characters
        opening_tag = data.get("opening-tag", "{")
        closing_tag = data.get("closing-tag", "}")

        # Extract tag mappings, text limits, and default colors
        tag_mappings = {}
        text_limits = {}
        default_colors = {}
        for tag, props in data.items():
            if tag in ["opening-tag", "closing-tag"]:
                continue
            if not isinstance(props,
                              dict) or "htmlTag" not in props or "text_limit" not in props or "default-color" not in props:
                raise ValueError(
                    f"Invalid configuration for tag '{tag}': missing 'htmlTag', 'text_limit', or 'default-color'")
            tag_mappings[tag] = props["htmlTag"]
            text_limits[tag] = props["text_limit"]

            # Validate default-color
            color = props["default-color"]
            if not isinstance(color, list) or len(color) != 3 or not all(
                    isinstance(c, int) and 0 <= c <= 255 for c in color):
                raise ValueError(f"Invalid 'default-color' for tag '{tag}': must be a list of three integers (0-255)")
            default_colors[tag] = tuple(color)

        # Validate root tag
        if "root" not in tag_mappings:
            raise ValueError("Missing 'root' tag in JSON configuration")

        return tag_mappings, text_limits, default_colors, opening_tag, closing_tag
    except FileNotFoundError:
        raise ValueError(f"JSON file {json_file} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {json_file}")
    except KeyError as e:
        raise ValueError(f"Missing required key in JSON: {e}")