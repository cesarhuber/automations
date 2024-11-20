from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tkinter as tk
import threading
import time


class BlingAutomation:
    def __init__(self):
        self.driver = None

    def init_browser(self):
        """Inicializa o navegador com as configurações necessárias."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Abrir o navegador em tela cheia
        self.driver = webdriver.Chrome(options=options)

    def open_login_page(self):
        """Abre a página de login do Bling para o usuário fazer o login manualmente."""
        self.driver.get("https://www.bling.com.br/login")
        print("Por favor, realize o login manualmente no navegador.")

    def access_checkout_page(self):
        """Acessa a tela de checkout de vendas e interage com a caixa de texto."""
        try:
            # Acessa a página de vendas
            self.driver.get("https://www.bling.com.br/vendas.checkout.php")
            
            # Espera o carregamento da página
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="itemCode"]')))
            
            # Fecha possíveis prompts
            try:
                prompt_close_buttons = self.driver.find_elements(By.CLASS_NAME, "close-button-class")
                for button in prompt_close_buttons:
                    button.click()
            except NoSuchElementException:
                print("Nenhum prompt encontrado.")

            # Interage com o elemento desejado
            caixa_texto = self.driver.find_element(By.XPATH, '//*[@id="itemCode"]')
            caixa_texto.click()
            print("Caixa de texto encontrada e selecionada.")
        except TimeoutException:
            print("Erro: Não foi possível carregar a tela ou encontrar a caixa de texto.")
        except Exception as e:
            print("Erro inesperado:", e)

    def end(self):
        """Encerra o navegador."""
        if self.driver:
            self.driver.quit()


class AutomationInterface:
    def __init__(self, automation):
        self.automation = automation
        self.root = tk.Tk()
        self.root.title("Automação Bling")
        self.root.geometry("300x200")

        # Botões da interface
        self.btn_login = tk.Button(self.root, text="Abrir Login", command=self.open_login)
        self.btn_login.pack(pady=10)

        self.btn_iniciar = tk.Button(self.root, text="Iniciar Automação", command=self.init_automation, state=tk.DISABLED)
        self.btn_iniciar.pack(pady=10)

        self.btn_finalizar = tk.Button(self.root, text="Finalizar", command=self.end)
        self.btn_finalizar.pack(pady=10)

    def open_login(self):
        """Abre a página de login do Bling e habilita o botão de iniciar."""
        threading.Thread(target=self.automation.open_login_page).start()
        self.btn_iniciar.config(state=tk.NORMAL)  # Habilita o botão Iniciar após abrir o login

    def init_automation(self):
        """Executa a automação após o login."""
        threading.Thread(target=self.automation.access_checkout_page).start()

    def end(self):
        """Finaliza a automação e fecha a interface."""
        self.automation.end()
        self.root.destroy()

    def init_interface(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()


# Main
if __name__ == "__main__":
    automation = BlingAutomation()
    automation.init_browser()
    interface = AutomationInterface(automation)
    interface.init_interface()