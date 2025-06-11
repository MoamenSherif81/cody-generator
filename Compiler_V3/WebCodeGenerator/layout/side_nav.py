from typing import List


def add_side_nav(args: List[str]) -> (str, str):
    # Side nav links
    elements = ""
    if len(args) != 0:
        elements = '<ul class="side-nav-list">'
        if isinstance(args, str):
            elements += f'<li><a href="#{args}" class="side-nav-item">{args}</a></li>'
        else:
            ar = []
            for arg in args:
                if arg == ',':
                    continue
                ar.append(arg)
            for arg in ar:
                elements += f'<li><a href="#{arg}" class="side-nav-item">{arg}</a></li>'
        elements += '</ul>'

    # Side Nav HTML structure
    html = f"""
    <div class="side-nav">
        <div class="side-nav-container">
            <div class="side-nav-logo">
                <a href="#" class="side-nav-logo-link">Logo</a>
            </div>
            {elements}
        </div>
    </div>
    """

    # Side Nav CSS with distinct and clean styling
    css = """
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
    z-index: 100; /* Keep sidebar above content */
}

.side-nav-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
    padding: 20px;
}

/* Main content adjustment */
.main-content {
    margin-left: 16%;  /* Makes space for the side nav */
    padding: 20px;
    width: calc(100% - 16%); /* Ensures content doesn't overflow */
}

/* Footer, navigation, etc. */
.side-nav-logo-link {
    font-size: 1.5rem;
    color: #4a90e2;
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
    color: #4a90e2;
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
    background-color: #4a90e2;
    color: white;
}
    """

    return html, css
