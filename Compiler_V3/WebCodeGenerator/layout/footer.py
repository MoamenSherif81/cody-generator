from typing import List


def add_footer(args: List[str]) -> (str, str):
    # Footer links logic (same as your original code)
    elements = ""
    if len(args) != 0:
        elements = '<nav class="footer-nav"><ul class="footer-nav-list">'

        # If args is a single string, add it as a single link
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="footer-nav-item">{args}</a></li>'
        else:
            # Iterate through the list and add each item as a navigation link
            ar = [arg for arg in args if arg != ',']
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="footer-nav-item">{arg}</a></li>'

        elements += '</ul></nav>'

    # Footer HTML structure
    html = f"""
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-logo">
                <a href="#" class="footer-logo-link">Logo</a>
            </div>
            {elements}
            <div class="footer-cta">
                <a href="#contact" class="footer-cta-button">Contact Us</a>
            </div>
        </div>
    </footer>
    """

    # Footer CSS with consistent design from the header
    css = """
    .footer {
        background-color: #ffffff;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
        padding: 16px 20px;
        margin-top: 40px;
        border-radius: 15px;
    }

    .footer-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    .footer-logo-link {
        font-size: 1.5rem;
        color: #00796b;  /* Matching the logo color */
        text-decoration: none;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* Navigation Styling */
    .footer-nav {
        flex: 1;
        display: flex;
        justify-content: center;
    }

    .footer-nav-list {
        list-style-type: none;
        display: flex;
        gap: 20px;
    }

    .footer-nav-item {
        text-decoration: none;
        font-size: 1rem;
        color: #333;
        padding: 8px 16px;
        transition: color 0.3s ease, background-color 0.3s ease;
    }

    .footer-nav-item:hover {
        color: #00796b;  /* Matching header hover color */
        background-color: #f1f1f1;
        border-radius: 5px;
    }

    /* Call to Action Button */
    .footer-cta {
        display: flex;
        align-items: center;
    }

    .footer-cta-button {
        padding: 12px 24px;
        background-color: #00796b;
        color: #ffffff;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .footer-cta-button:hover {
        background-color: #004d40;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .footer-container {
            flex-direction: column;
            align-items: flex-start;
        }

        .footer-nav-list {
            flex-direction: column;
            gap: 12px;
        }

        .footer-cta-button {
            width: 100%;
            padding: 10px;
            text-align: center;
        }
    }
    """

    return html, css
