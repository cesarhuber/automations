from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import platform

def get_browser_binary():
    """Detects the installed browser and returns its path."""
    current_os = platform.system()

    if current_os == "Darwin":  # macOS
        possible_browsers = {
            "Brave": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "Arc": "/Applications/Arc.app/Contents/MacOS/Arc",
            "Chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        }
    elif current_os == "Linux":  # Linux
        possible_browsers = {
            "Brave": "/usr/bin/brave",
            "Arc": "/usr/bin/arc",  # Ensure correct path for Arc
            "Chrome": "/usr/bin/google-chrome"
        }
    elif current_os == "Windows":  # Windows
        possible_browsers = {
            "Brave": "C:\\Program Files\\Brave Software\\Brave-Browser\\Application\\brave.exe",
            "Arc": "C:\\Program Files\\Arc\\Arc.exe",  # Ensure correct path for Arc
            "Chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        }
    else:
        raise OSError(f"Unsupported OS: {current_os}")

    # Check for installed browser
    for browser, path in possible_browsers.items():
        if os.path.exists(path):
            print(f"{browser} found at {path}")
            return path  # Return the first found browser path

    # Raise error if no compatible browser is found
    raise FileNotFoundError("No compatible Chromium-based browser found.")

def setup_driver():
    """Sets up the WebDriver with the appropriate browser configuration."""
    chrome_options = Options()

    # Get the correct browser binary based on the OS
    browser_binary = get_browser_binary()
    
    # Configure the browser path for Selenium
    chrome_options.binary_location = browser_binary

    # Use webdriver-manager to automatically fetch the correct ChromeDriver version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver