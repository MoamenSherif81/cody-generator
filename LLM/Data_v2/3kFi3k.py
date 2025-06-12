#!/usr/bin/env python3
"""
Brave Browser Controller for Ubuntu
This script connects to your existing Brave browser instance to automate tasks
while preserving your logged-in sessions and cookies.
"""

import subprocess
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class BraveController:
    def __init__(self, debug_port=9222):
        self.debug_port = debug_port
        self.driver = None
        self.debug_url = f"http://localhost:{debug_port}"

    def start_brave_with_debugging(self):
        """Start Brave with remote debugging enabled"""
        try:
            # Kill existing Brave processes to ensure clean start
            subprocess.run(["pkill", "-f", "brave"], check=False)
            time.sleep(2)

            # Start Brave with remote debugging
            brave_cmd = [
                "brave",
                f"--remote-debugging-port={self.debug_port}",
                "--remote-allow-origins=*",
                "--disable-web-security",
                "--user-data-dir=/home/$USER/.config/BraveSoftware/Brave-Browser/Default"
            ]

            print(f"Starting Brave with debugging on port {self.debug_port}...")
            subprocess.Popen(brave_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)

            # Verify debugging is working
            response = requests.get(f"{self.debug_url}/json")
            if response.status_code == 200:
                print("✓ Brave debugging interface is active")
                return True
            else:
                print("✗ Failed to connect to Brave debugging interface")
                return False

        except Exception as e:
            print(f"Error starting Brave: {e}")
            return False

    def connect_to_existing_brave(self):
        """Connect to existing Brave instance with debugging enabled"""
        try:
            response = requests.get(f"{self.debug_url}/json")
            if response.status_code == 200:
                print("✓ Connected to existing Brave instance")
                return True
            else:
                print("✗ No debugging interface found. Starting new instance...")
                return self.start_brave_with_debugging()
        except requests.exceptions.ConnectionError:
            print("✗ No debugging interface found. Starting new instance...")
            return self.start_brave_with_debugging()

    def get_browser_tabs(self):
        """Get list of open tabs"""
        try:
            response = requests.get(f"{self.debug_url}/json")
            tabs = response.json()
            print(f"Found {len(tabs)} open tabs:")
            for i, tab in enumerate(tabs):
                print(f"  {i}: {tab.get('title', 'No title')} - {tab.get('url', 'No URL')}")
            return tabs
        except Exception as e:
            print(f"Error getting tabs: {e}")
            return []

    def setup_selenium_driver(self):
        """Setup Selenium WebDriver to connect to existing Brave instance"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")

            # You might need to specify the path to chromedriver
            # Download from: https://chromedriver.chromium.org/
            service = Service()  # Add path if needed: Service("/path/to/chromedriver")

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ Selenium connected to Brave instance")
            return True

        except WebDriverException as e:
            print(f"✗ Selenium connection failed: {e}")
            print("Make sure you have chromedriver installed:")
            print("  sudo apt install chromium-chromedriver")
            print("  or download from https://chromedriver.chromium.org/")
            return False

    def navigate_to_url(self, url):
        """Navigate to a specific URL"""
        if not self.driver:
            print("Driver not initialized. Call setup_selenium_driver() first.")
            return False

        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            print(f"Navigation failed: {e}")
            return False

    def find_element_and_click(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Find element and click it"""
        if not self.driver:
            print("Driver not initialized.")
            return False

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            print(f"✓ Clicked element: {selector}")
            return True
        except TimeoutException:
            print(f"✗ Element not found or not clickable: {selector}")
            return False

    def get_page_title(self):
        """Get current page title"""
        if not self.driver:
            return None
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        if not self.driver:
            return None
        return self.driver.current_url

    def execute_javascript(self, script):
        """Execute JavaScript in the browser"""
        if not self.driver:
            print("Driver not initialized.")
            return None

        try:
            result = self.driver.execute_script(script)
            return result
        except Exception as e:
            print(f"JavaScript execution failed: {e}")
            return None

    def take_screenshot(self, filename="screenshot.png"):
        """Take screenshot of current page"""
        if not self.driver:
            print("Driver not initialized.")
            return False

        try:
            self.driver.save_screenshot(filename)
            print(f"✓ Screenshot saved as {filename}")
            return True
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return False

    def close(self):
        """Close the connection (keeps browser open)"""
        if self.driver:
            self.driver.quit()
            print("✓ Connection closed")


def main():
    """Example usage"""
    controller = BraveController()

    # Try to connect to existing Brave instance
    if not controller.connect_to_existing_brave():
        print("Failed to connect to Brave")
        return

    # Get list of open tabs
    controller.get_browser_tabs()

    # Setup Selenium connection
    if not controller.setup_selenium_driver():
        print("Failed to setup Selenium driver")
        return

    # Example automation tasks
    print(f"\nCurrent page: {controller.get_page_title()}")
    print(f"Current URL: {controller.get_current_url()}")

    # Navigate to a new page (optional)
    # controller.navigate_to_url("https://www.google.com")

    # Take a screenshot
    controller.take_screenshot("current_page.png")

    # Execute some JavaScript
    result = controller.execute_javascript("return document.title;")
    print(f"Page title via JS: {result}")

    # Keep connection open for manual use
    print("\nBrowser connection is active. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        controller.close()


if __name__ == "__main__":
    main()