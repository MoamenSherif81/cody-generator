import os
import glob
import queue
import sys
from queue import Queue, Empty
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from Compiler_V2 import compile_dsl

def setup_chrome_driver():
    """Set up headless Chrome driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def screenshot_worker(task_queue, result_queue, progress_bar):
    """Worker function: process .gui files from task queue, take screenshots, and push to result queue."""
    thread_local = threading.local()
    thread_local.driver = setup_chrome_driver()
    try:
        while True:
            try:
                gui_file = task_queue.get_nowait()
            except Empty:
                break  # Task queue is empty, exit thread
            try:
                # Read .gui file content
                with open(gui_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Compile to HTML and CSS
                html_content, css_content = compile_dsl(content)
                # Combine HTML and CSS
                html_with_css = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>{css_content}</style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                # Inject HTML into blank page
                thread_local.driver.get("about:blank")
                thread_local.driver.execute_script(f"document.documentElement.innerHTML = {repr(html_with_css)};")
                # Capture screenshot as bytes
                screenshot_data = thread_local.driver.get_screenshot_as_png()
                output_png = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(gui_file))[0]}.png")
                # Push to result queue
                result_queue.put((screenshot_data, output_png))
            except Exception as e:
                print(f"Error processing {gui_file}: {str(e)}")
            finally:
                task_queue.task_done()
                with progress_bar.get_lock():
                    progress_bar.update(1)
    finally:
        thread_local.driver.quit()

def write_worker(result_queue):
    """Worker function: write screenshots from result queue to disk."""
    while True:
        try:
            screenshot_data, output_path = result_queue.get_nowait()
            with open(output_path, 'wb') as f:
                f.write(screenshot_data)
            result_queue.task_done()
        except Empty:
            break  # Result queue is empty, exit thread

def main(input_folder, output_folder, screenshot_ratio=0.33):
    """Main function to process .gui files using two queues and multithreading."""
    global output_dir
    output_dir = output_folder  # Make output_dir accessible to workers

    # Start timer
    start_time = time.time()

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all .gui files
    gui_files = glob.glob(os.path.join(input_folder, "*.gui"))
    if not gui_files:
        print("No .gui files found in the input folder.")
        return

    # Initialize queues
    task_queue = Queue()
    result_queue = Queue()
    for gui_file in gui_files:
        task_queue.put(gui_file)

    # Set total workers based on CPU count (doubled for I/O-bound tasks)
    total_workers = os.cpu_count() * 2 if os.cpu_count() else 4

    # Calculate number of screenshot and write workers
    screenshot_workers = max(1, int(total_workers * screenshot_ratio))
    write_workers = max(1, total_workers - screenshot_workers)

    # Initialize progress bar
    progress_bar = tqdm(total=len(gui_files), desc="Processing .gui files", unit="file")

    # Start worker threads
    with ThreadPoolExecutor(max_workers=total_workers) as executor:
        screenshot_futures = [
            executor.submit(screenshot_worker, task_queue, result_queue, progress_bar)
            for _ in range(screenshot_workers)
        ]
        write_futures = [
            executor.submit(write_worker, result_queue)
            for _ in range(write_workers)
        ]
        for future in screenshot_futures + write_futures:
            future.result()

    # Close progress bar
    progress_bar.close()

    # Calculate and print execution time
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    main(input_folder, output_folder, screenshot_ratio=0.33)