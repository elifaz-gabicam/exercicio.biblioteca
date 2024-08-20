import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Configura o WebDriver e garante o fechamento após o teste
    driver = webdriver.Firefox()  # Ou use webdriver.Chrome() se estiver usando o Chrome
    yield driver
    driver.quit()

def test_home_page(driver):
    driver.get("http://127.0.0.1:5000/curriculo")  # Acessa a página do currículo

    # Espera até que o texto "Currículo Vitae" esteja presente na página
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Currículo Vitae')]"))
    )

    assert "Currículo Vitae" in driver.page_source  # Verifica se "Currículo Vitae" está na página

def test_user_login(driver):
    driver.get("http://127.0.0.1:5000/login")  # Acessa a página de login

    # Espera até que os campos de entrada estejam visíveis
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("elifaz.gabi@gmail.com")  # Digita o nome de usuário

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("elifazgc2024")  # Digita a senha

    password_input.send_keys(Keys.RETURN)  # Simula o Enter para submeter o formulário

    # Espera até que o texto "Biblioteca" esteja presente na página
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Biblioteca')]"))
    )

    assert "Biblioteca" in driver.page_source  # Verifica se o login foi bem-sucedido
