from typing import List, Tuple, Union
from string import Template

def add_side_nav(
        args: Union[List[str], str] = [],
        logo_text: str = "Logo",
        main_color: str = "#4a90e2",
        dark_color: str = "#357abd"
) -> Tuple[str, str]:
    """
    Generate HTML and CSS for a responsive side navigation bar with dynamic links.

    Args:
        args: List of navigation item names or single string
        logo_text: Text to display as the logo
        main_color: Primary color for the theme (default: blue)
        dark_color: Darker shade for hover effects (default: dark blue)

    Returns:
        Tuple containing (HTML string, CSS string)
    """
    # Generate navigation links with original preprocessing
    elements = ""
    if len(args) != 0:
        elements = '<ul class="side-nav-list">'
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="side-nav-item">{args}</a></li>'
        else:
            ar = [arg for arg in args if arg != ',']
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="side-nav-item">{arg}</a></li>'
        elements += '</ul>'

    # Updated HTML template with toggle functionality
    html_template = Template("""
    <input type="checkbox" id="side-nav-toggle" class="side-nav-toggle-input">
    <label for="side-nav-toggle" class="side-nav-toggle-label">☰</label>
    <div class="side-nav">
        <div class="side-nav-container">
            <label for="side-nav-toggle" class="side-nav-close-label">×</label>
            <div class="side-nav-logo">
                <a href="#" class="side-nav-logo-link">$logo_text</a>
            </div>
            $nav_html
        </div>
    </div>
    """)

    html = html_template.substitute(logo_text=logo_text, nav_html=elements)

    # Updated CSS template with responsive design
    css_template = Template("""
.side-nav {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 15%;
    background-color: #ffffff;
    color: #333;
    border-right: 1px solid #e0e0e0;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    padding-top: 20px;
    z-index: 100;
    transform: translateX(0);
    transition: transform 0.3s ease;
}

.side-nav-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
    padding: 20px;
}

.main-content {
    margin-left: 16%;
    padding: 20px;
    width: calc(100% - 16%);
}

.side-nav-logo-link {
    font-size: 1.5rem;
    color: $main_color;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    text-align: center;
}

.side-nav-list {
    list-style-type: none;
    padding: 0;
    margin-top: 20px;
}

.side-nav-item {
    color: #333;
    text-decoration: none;
    font-size: 1.1rem;
    padding: 12px 20px;
    display: block;
    transition: background-color 0.3s, color 0.3s;
    border-radius: 5px;
}

.side-nav-item:hover {
    background-color: #f0f4f8;
    color: $main_color;
}

.side-nav-footer {
    margin-top: auto;
    text-align: center;
    padding: 20px;
}

.side-nav-footer-link {
    font-size: 1rem;
    color: #333;
    text-decoration: none;
    display: inline-block;
    padding: 10px 15px;
    background-color: #f0f4f8;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

.side-nav-footer-link:hover {
    background-color: $dark_color;
    color: white;
}

.side-nav-toggle-input {
    display: none;
}

.side-nav-toggle-label {
    display: none;
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 101;
    cursor: pointer;
    font-size: 1.5rem;
    padding: 10px;
}

.side-nav-close-label {
    display: none;
    cursor: pointer;
    font-size: 1.5rem;
    padding: 10px;
    text-align: right;
}

@media (max-width: 768px) {
    .side-nav {
        transform: translateX(-100%);
        width: 80%;
    }
    .side-nav-toggle-label {
        display: block;
    }
    .side-nav-toggle-input:checked ~ .side-nav {
        transform: translateX(0);
    }
    .side-nav-close-label {
        display: block;
    }
    .main-content {
        margin-left: 0;
        width: 100%;
    }
}
    """)

    css = css_template.substitute(main_color=main_color, dark_color=dark_color)

    return html, css