from typing import List


def add_header(args: List[str]) -> (str, str):
    # Initialize elements for the dynamic navigation links
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

    # Header HTML structure
    html = f"""
    <header class="header">
        <div class="container">
            <div class="logo-container">
                <a href="#" class="logo-link">Logo</a>
            </div>
            {elements}
        </div>
    </header>
    """

    # Refactored CSS for modern and minimal styling
    css = """
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
        color: #00796b;
        text-decoration: none;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* Navigation Styling */
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
        color: #00796b;
        background-color: #f1f1f1;
        border-radius: 5px;
    }

    /* Call to Action Button */
    .cta {
        display: flex;
        align-items: center;
    }

    .cta-button {
        padding: 12px 24px;
        background-color: #00796b;
        color: #ffffff;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .cta-button:hover {
        background-color: #004d40;
    }

    /* Responsive Design */
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
    """

    return html, css
