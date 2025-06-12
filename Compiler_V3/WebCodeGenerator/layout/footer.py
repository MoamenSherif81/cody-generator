from typing import List, Tuple, Union
from string import Template

def add_footer(
        args: Union[List[str], str] = [],
        logo_text: str = "Logo",
        main_color: str = "#00796b",
        dark_color: str = "#004d40"
) -> Tuple[str, str]:
    """
    Generate HTML and CSS for a responsive footer with dynamic navigation links.

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
        elements = '<nav class="footer-nav"><ul class="footer-nav-list">'
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="footer-nav-item">{args}</a></li>'
        else:
            ar = [arg for arg in args if arg != ',']
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="footer-nav-item">{arg}</a></li>'
        elements += '</ul></nav>'

    # HTML template
    html_template = Template("""
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-logo">
                <a href="#" class="footer-logo-link">$logo_text</a>
            </div>
            $nav_html
            <div class="footer-cta">
                <a href="#contact" class="footer-cta-button">Contact Us</a>
            </div>
        </div>
    </footer>
    """)

    html = html_template.substitute(logo_text=logo_text, nav_html=elements)

    css_template = Template("""
    .footer {
        background: #fff;
        box-shadow: 0 -4px 16px rgba(0,0,0,0.09);
        padding: 32px 0 22px 0;
        margin-top: 56px;
        border-radius: 18px 18px 0 0;
        width: 100%;
        position: relative;
        z-index: 10;
        overflow-x: auto;
    }

    .footer-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        gap: 36px;
        padding: 0 24px;
        min-width: 0;
        flex-wrap: wrap;
        box-sizing: border-box;
    }

    .footer-logo,
    .footer-nav,
    .footer-cta {
        min-width: 0;
        max-width: 100%;
        box-sizing: border-box;
    }
    .footer-logo {
        flex: 0 1 auto;
    }
    .footer-logo-link {
        font-size: 1.4rem;
        color: $main_color;
        text-decoration: none;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        transition: color 0.3s;
        display: inline-block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }

    .footer-nav {
        flex: 1 1 0;
        display: flex;
        justify-content: center;
        min-width: 0;
        overflow: hidden;
    }
    .footer-nav-list {
        list-style-type: none;
        display: flex;
        gap: 24px;
        margin: 0;
        padding: 0;
        min-width: 0;
        overflow: hidden;
    }
    .footer-nav-item {
        text-decoration: none;
        font-size: 1.05rem;
        color: #313131;
        padding: 7px 18px;
        border-radius: 7px;
        transition: color 0.2s, background 0.2s;
        font-weight: 500;
        cursor: pointer;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    .footer-nav-item:hover,
    .footer-nav-item:focus {
        color: $main_color;
        background: #f3f6f6;
    }

    .footer-cta {
        flex: 0 1 auto;
        min-width: 0;
        display: flex;
        align-items: center;
        max-width: 100%;
    }
    .footer-cta-button {
        padding: 12px 30px;
        background: $main_color;
        color: #fff;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        transition: background 0.25s;
        border: none;
        cursor: pointer;
        display: inline-block;
        letter-spacing: 0.8px;
        max-width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .footer-cta-button:hover,
    .footer-cta-button:focus {
        background: $dark_color;
    }

    @media (max-width: 900px) {
        .footer-container {
            gap: 18px;
            padding: 0 10px;
        }
        .footer-nav-list {
            gap: 10px;
        }
        .footer-logo-link {
            font-size: 1.07rem;
        }
        .footer-cta-button {
            font-size: 0.95rem;
            padding: 11px 16px;
        }
    }

    @media (max-width: 700px) {
        .footer {
            padding: 20px 0 12px 0;
            border-radius: 12px 12px 0 0;
        }
        .footer-container {
            flex-direction: column;
            align-items: flex-start;
            justify-content: flex-start;
            gap: 0;
            padding: 0 3vw;
        }
        .footer-logo {
            margin-bottom: 10px;
            width: 100%;
        }
        .footer-nav {
            width: 100%;
            justify-content: flex-start;
            margin-bottom: 10px;
            display: block;
            overflow: visible;
        }
        .footer-nav-list {
            display: flex;
            flex-direction: column;
            width: 100%;
            margin: 0;
            padding: 0;
        }
        .footer-nav-item {
            padding: 13px 0;
            font-size: 1.05rem;
            width: 100%;
            border-radius: 0;
            border-bottom: 1px solid #f3f3f3;
            white-space: normal;
        }
        .footer-nav-item:last-child {
            border-bottom: none;
        }
        .footer-cta {
            width: 100%;
            margin-top: 10px;
            justify-content: flex-start;
        }
        .footer-cta-button {
            width: 100%;
            text-align: center;
            font-size: 1.05rem;
            padding: 13px 0;
        }
    }
    """)

    css = css_template.substitute(main_color=main_color, dark_color=dark_color)

    return html, css