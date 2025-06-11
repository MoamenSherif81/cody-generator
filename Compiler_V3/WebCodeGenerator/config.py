import json
from dataclasses import dataclass
from typing import Dict, List, Tuple


# Define the class for the configuration of each tag
@dataclass
class TagConfig:
    htmlTag: str
    cssClasses: List[str]
    cssAttributes: Dict[str, str]
    textLimit: int
    defaultColor: Tuple[int, int, int]


# Define the class to hold the entire configuration
@dataclass
class Config:
    tagMappings: Dict[str, TagConfig]
    openingTag: str
    closingTag: str

    @staticmethod
    def from_json(file_path: str):
        """Static method to load a Config from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)

            # Map the tags
            tag_mappings = {
                tag: TagConfig(
                    htmlTag=tag_data.get("htmlTag", ""),
                    cssClasses=tag_data.get("cssClasses", []),
                    cssAttributes=tag_data.get("cssAttributes", {}),
                    textLimit=tag_data.get("textLimit", 0),
                    defaultColor=tuple(tag_data.get("defaultColor", [0, 0, 0]))
                )
                for tag, tag_data in config_data.get("tagMappings", {}).items()
            }
            return tag_mappings, "{", "}"

        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {file_path}")
