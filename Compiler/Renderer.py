import os
import re
import time
import sys
import asyncio
from playwright.async_api import async_playwright
from compiler import compiler
from tqdm import tqdm

SEM_LIMIT = os.cpu_count()  # Number of concurrent operations

def extract_body_content(html):
    """Extracts the content inside the <body> tag from an HTML string."""
    match = re.search(r"<body.*?>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else ""


async def process_file(file_path, output_directory, css_file_content, browser, semaphore, progress_bar):
    """
    Processes a single `.gui` file, compiles it to HTML, and captures a screenshot.

    :param file_path: Path to the `.gui` file.
    :param output_directory: Directory to store the output images.
    :param css_file_content: CSS styles to be applied.
    :param browser: Playwright browser instance.
    :param semaphore: Semaphore to control concurrency.
    :param progress_bar: tqdm progress bar instance.
    """
    async with semaphore:
        compiler_instance = compiler(output_directory)
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        html_content = compiler_instance.compile(content)
        html_content = extract_body_content(html_content)

        full_html = f"""
        <html>
        <head>
            <style>{css_file_content}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        output_image_path = os.path.join(
            output_directory,
            f"{os.path.splitext(os.path.basename(file_path))[0]}.png"
        )
        await page.set_content(full_html)
        await page.screenshot(path=output_image_path, full_page=False)

        await page.close()
        await context.close()

        # Update progress bar in a thread-safe manner
        with progress_bar.get_lock():
            progress_bar.update(1)


async def do_work(directory_path, output_directory, css_file_content, thread_count=5):
    """
    Processes all `.gui` files in the directory concurrently using asyncio.

    :param directory_path: Path to the directory containing `.gui` files.
    :param output_directory: Path to store the output images.
    :param css_file_content: CSS styles to be applied.
    :param thread_count: Number of concurrent tasks (default: 5).
    """
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return

    os.makedirs(output_directory, exist_ok=True)
    gui_files = [
        os.path.join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.endswith(".gui")
    ]

    semaphore = asyncio.Semaphore(thread_count)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Initialize progress bar
        progress_bar = tqdm(total=len(gui_files), desc="Processing .gui files", unit="file")

        tasks = [
            process_file(file_path, output_directory, css_file_content, browser, semaphore, progress_bar)
            for file_path in gui_files
        ]
        await asyncio.gather(*tasks)

        # Close progress bar
        progress_bar.close()
        await browser.close()


if __name__ == "__main__":
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    css_file_path = "style.css"

    with open(css_file_path, "r", encoding="utf-8") as css_file:
        css_content = css_file.read()

    start_time = time.time()
    asyncio.run(do_work(input_directory, output_directory, css_content, thread_count=os.cpu_count()))
    end_time = time.time()

    total_time = end_time - start_time
    print(f"All files processed successfully in {total_time:.2f} seconds!")