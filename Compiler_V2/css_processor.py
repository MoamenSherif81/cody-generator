from typing import Set, List

import cssutils


def filter_css(css_file: str, used_classes: Set[str]) -> str:
    """Filter CSS file to include only rules for used classes."""
    try:
        with open(css_file, "r") as f:
            css_content = f.read()
    except FileNotFoundError:
        return ""

    rules = []
    current_rule = ""
    in_rule = False
    brace_count = 0

    for line in css_content.splitlines():
        line = line.strip()
        if not line:
            continue

        if not in_rule and "{" in line:
            in_rule = True
            current_rule = line
            brace_count = line.count("{") - line.count("}")
        elif in_rule:
            current_rule += " " + line
            brace_count += line.count("{") - line.count("}")
            if brace_count == 0:
                in_rule = False
                for cls in used_classes:
                    if f".{cls}" in current_rule:
                        rules.append(current_rule)
                        break
                current_rule = ""

    return "\n".join(rules)


def generate_css_template(css_content: str, dynamic_css_rules: List[str] = None) -> str:
    """Wrap CSS content and append dynamic CSS rules."""
    combined_css = """
    *{
      margin: 0;
      box-sizing: border-box;
    }
    
    body{
      padding: 24px;
      background-color: white;
      font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }\n
    """
    combined_css += css_content
    if dynamic_css_rules:
        combined_css += "\n\n" + "\n".join(dynamic_css_rules)
    combined_css += """\n
    @media (max-width: 1024px){
      .row{
        flex-direction: column;
      }
    }
    """
    sheet = cssutils.parseString(combined_css, validate=False)
    formatted_css = sheet.cssText.decode("utf-8")  # Convert from bytes to string
    return formatted_css
