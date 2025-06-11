from typing import List, Tuple, Union
from string import Template


def add_header(
        args: Union[List[str], str] = [],
        logo_text: str = "Logo",
        main_color: str = "#00796b",
        dark_color: str = "#004d40"
) -> Tuple[str, str]:
    """
    Generate HTML and CSS for a responsive header with dynamic navigation links.

    Args:
        args: List of navigation item names or single string
        logo_text: Text to display as the logo
        main_color: Primary color for the theme (default: teal)
        dark_color: Darker shade for hover effects (default: dark teal)

    Returns:
        Tuple containing (HTML string, CSS string)
    """
    # Generate navigation links with original preprocessing
    elements = ""
    if len(args) != 0:
        elements = '<nav class="nav"><ul class="nav-list">'

        # If args is a single string, add it as a single link
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="nav-item">{args}</a></li>'
        else:
            # Iterate through the list and add each item as a navigation link
            ar = [arg for arg in args if arg != ',']
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="nav-item">{arg}</a></li>'

        elements += '</ul></nav>'

    # HTML template
    html_template = Template("""
    <header class="header">
        <div class="container">
            <div class="logo-container">
                <a href="#" class="logo-link">$logo_text</a>
            </div>
            $nav_html
        </div>
    </header>
    """)

    html = html_template.substitute(logo_text=logo_text, nav_html=elements)

    # CSS template
    css_template = Template("""
    .header {
        padding-right: 5%;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 16px 20px;
        margin-bottom: 2%;
        border-radius: 15px;
    }

    .container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }

    .logo-container {
        flex: 1;
        display: flex;
        align-items: center;
    }

    .logo-link {
        font-size: 1.5rem;
        color: $main_color;
        text-decoration: none;
        font-weight: bold;
        text-transform: uppercase;
    }

    .nav-list {
        list-style-type: none;
        display: flex;
        gap: 20px;
        margin: 0;
        padding: 0;
    }

    .nav-item {
        text-decoration: none;
        font-size: 1rem;
        color: #333;
        padding: 8px 16px;
        transition: color 0.3s ease, background-color 0.3s ease;
    }

    .nav-item:hover {
        color: $main_color;
        background-color: #f1f1f1;
        border-radius: 5px;
    }

    .cta {
        display: flex;
        align-items: center;
    }

    .cta-button {
        padding: 12px 24px;
        background-color: $main_color;
        color: #ffffff;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .cta-button:hover {
        background-color: $dark_color;
    }

    @media (max-width: 768px) {
        .container {
            flex-direction: column;
            align-items: flex-start;
        }

        .nav-list {
            flex-direction: column;
            gap: 12px;
        }

        .cta-button {
            width: 100%;
            padding: 10px;
            text-align: center;
        }
    }
    """)

    css = css_template.substitute(main_color=main_color, dark_color=dark_color)

    return html, css