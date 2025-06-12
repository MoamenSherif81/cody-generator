from typing import List, Tuple, Union
from string import Template

def add_header(
        args: Union[List[str], str] = [],
        logo_text: str = "Logo",
        main_color: str = "#00796b",
        dark_color: str = "#004d40"
) -> Tuple[str, str]:
    """
    Generate HTML and CSS for a responsive header with dynamic navigation links and a hamburger menu for mobile.

    Args:
        args: List of navigation item names or single string
        logo_text: Text to display as the logo
        main_color: Primary color for the theme (default: teal)
        dark_color: Darker shade for hover effects (default: dark teal)

    Returns:
        Tuple containing (HTML string, CSS string)
    """
    # Generate navigation links
    elements = ""
    if len(args) != 0:
        elements = '<nav class="nav"><ul class="nav-list">'
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="nav-item">{args}</a></li>'
        else:
            ar = [arg for arg in args if arg != ',']
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="nav-item">{arg}</a></li>'
        elements += '</ul></nav>'

    # HTML template with hamburger menu and nav toggle
    html_template = Template("""
    <header class="header">
        <input type="checkbox" id="menu-checkbox" style="display:none;">
        <div class="container">
            <div class="logo-container">
                <a href="#" class="logo-link">$logo_text</a>
            </div>
            <label for="menu-checkbox" class="menu-toggle">
                <span></span>
                <span></span>
                <span></span>
            </label>
            $nav_html
        </div>
    </header>
    """)

    html = html_template.substitute(logo_text=logo_text, nav_html=elements)

    # Modern, responsive CSS with hamburger and mobile nav
    css_template = Template("""
    .header {
        background: #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 18px 24px;
        border-radius: 16px;
        margin-bottom: 2%;
        width: 100%;
        position: relative;
        z-index: 10;
    }
    .container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }
    .logo-container {
        flex: 0 0 auto;
    }
    .logo-link {
        font-size: 1.7rem;
        font-weight: bold;
        text-decoration: none;
        color: $main_color;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: color 0.3s;
    }
    .nav {
        flex: 1 1 auto;
        display: flex;
        justify-content: flex-end;
        transition: none;
    }
    .nav-list {
        list-style: none;
        display: flex;
        gap: 24px;
        margin: 0;
        padding: 0;
    }
    .nav-item {
        text-decoration: none;
        font-size: 1rem;
        color: #222;
        padding: 8px 18px;
        border-radius: 6px;
        transition: color 0.2s, background 0.2s;
        position: relative;
        font-weight: 500;
        cursor: pointer;
        display: block;
    }
    .nav-item:hover,
    .nav-item:focus {
        color: $main_color;
        background: #f3f6f6;
    }
    /* Hamburger for mobile */
    .menu-toggle {
        display: none;
        flex-direction: column;
        justify-content: center;
        cursor: pointer;
        width: 40px;
        height: 40px;
        margin-left: 10px;
        z-index: 100;
    }
    .menu-toggle span {
        height: 4px;
        width: 28px;
        background: $main_color;
        margin: 4px 0;
        border-radius: 2px;
        display: block;
        transition: all 0.3s;
    }
    @media (max-width: 900px) {
        .container {
            padding: 0 10px;
        }
        .nav-list {
            gap: 16px;
        }
        .logo-link {
            font-size: 1.25rem;
        }
    }
    @media (max-width: 700px) {
        .header {
            padding: 10px 5px;
            border-radius: 10px;
        }
        .container {
            flex-direction: row;
            align-items: center;
            padding: 0 2px;
        }
        .logo-container {
            flex: 0 0 auto;
            margin-right: 8px;
        }
        .nav {
            position: absolute;
            top: 65px;
            right: 0;
            width: 100vw;
            background: #fff;
            box-shadow: 0 2px 16px rgba(0,0,0,0.13);
            border-radius: 0 0 14px 14px;
            transform: translateY(-150%);
            transition: transform 0.3s;
            z-index: 99;
            display: block;
        }
        .nav-list {
            flex-direction: column;
            gap: 0;
            padding: 8px 0 12px 0;
        }
        .nav-item {
            padding: 12px 22px;
            font-size: 1.09rem;
            width: 100%;
            border-radius: 0;
            border-bottom: 1px solid #f3f3f3;
        }
        .nav-item:last-child {
            border-bottom: none;
        }
        .menu-toggle {
            display: flex;
        }
    }
    /* CSS-only nav toggle */
    @media (max-width: 700px) {
        #menu-checkbox {
            display: none;
        }
        #menu-checkbox:checked ~ .container .nav {
            transform: translateY(0%);
            transition: transform 0.3s;
        }
        #menu-checkbox:checked ~ .container .menu-toggle span:nth-child(1) {
            transform: rotate(45deg) translate(6px, 6px);
        }
        #menu-checkbox:checked ~ .container .menu-toggle span:nth-child(2) {
            opacity: 0;
        }
        #menu-checkbox:checked ~ .container .menu-toggle span:nth-child(3) {
            transform: rotate(-45deg) translate(6px, -6px);
        }
    }
    """)

    css = css_template.substitute(main_color=main_color, dark_color=dark_color)
    return html, css
