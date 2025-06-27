from bs4 import BeautifulSoup
import cssutils
import re

def clean_and_format_html_css(html_code: str, css_code: str):
    # Parse HTML and collect used class names
    soup = BeautifulSoup(html_code, "html.parser")
    used_classes = set()
    for tag in soup.find_all(class_=True):
        for cls in tag.get("class"):
            used_classes.add(cls)

    # Parse CSS and build new stylesheet with only used classes
    css_parser = cssutils.CSSParser()
    sheet = css_parser.parseString(css_code)
    new_css = cssutils.css.CSSStyleSheet()
    class_selector_pattern = re.compile(r'\.([a-zA-Z0-9_-]+)')

    for rule in sheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split(",")
            keep = False
            for sel in selectors:
                match = class_selector_pattern.match(sel.strip())
                if match and match.group(1) in used_classes:
                    keep = True
            if keep:
                new_css.add(rule)

    # Format CSS (pretty print)
    formatted_css = new_css.cssText.decode("utf-8")

    # Format HTML (pretty print)
    formatted_html = soup.prettify()

    return formatted_html, formatted_css
