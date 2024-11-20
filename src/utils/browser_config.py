import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_browser_binary():
    """Detecta automaticamente o sistema operacional e o navegador instalado, e retorna o caminho."""
    # Obtém o sistema operacional atual
    current_os = platform.system()

    # Defina os caminhos dos navegadores para cada sistema operacional
    if current_os == "Darwin":  # macOS
        possible_browsers = {
            "Brave": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "Arc": "/Applications/Arc.app/Contents/MacOS/Arc",
            "Chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        }
    elif current_os == "Linux":  # Linux
        possible_browsers = {
            "Brave": "/usr/bin/brave",
            "Arc": "/usr/bin/arc",  # Ajuste conforme o caminho correto do Arc
            "Chrome": "/usr/bin/google-chrome"
        }
    elif current_os == "Windows":  # Windows
        possible_browsers = {
            "Brave": "C:\\Program Files\\Brave Software\\Brave-Browser\\Application\\brave.exe",
            "Arc": "C:\\Program Files\\Arc\\Arc.exe",  # Ajuste conforme o caminho do Arc no Windows
            "Chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        }
    else:
        raise OSError(f"Sistema operacional não suportado: {current_os}")

    # Verifica se algum dos navegadores está instalado no sistema
    for browser, path in possible_browsers.items():
        if os.path.exists(path):
            print(f"{browser} encontrado: {path}")
            return path  # Retorna o caminho do primeiro navegador encontrado

    # Se nenhum navegador for encontrado, levanta um erro
    raise FileNotFoundError("Nenhum navegador baseado em Chromium encontrado.")

def setup_driver():
    """Configura o WebDriver para o navegador detectado."""
    chrome_options = Options()

    # Obtém o caminho do navegador instalado
    browser_binary = get_browser_binary()
    
    # Configura o caminho do navegador no Selenium
    chrome_options.binary_location = browser_binary

    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver