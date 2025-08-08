from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entities.Livro import Livro
from back.Pdf import PDF

options = Options()
# options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")

# Cria corretamente o serviço do driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.amazon.com.br/s?k=fantasia&i=stripbooks&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91"

MAX_TENTATIVAS = 5

sucesso = False
tentativas = 0
listaLivros = []
pdfBuilder = PDF('Lista de Livros')

while not sucesso and tentativas < MAX_TENTATIVAS:
    print(f"Tentando carregar a página (tentativa {tentativas + 1})...")
    driver.get(url)
    tentativas += 1

    try:
        # Espera até que os produtos apareçam
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s-result-item"))
        )
        sucesso = True
        print("Página carregada com sucesso!")
    except:
        print("Erro ao carregar, tentando novamente...")
        time.sleep(2)

if not sucesso:
    print("❌ Não foi possível carregar a página após várias tentativas.")
    driver.quit()
    exit()


# print(len(itens))

# exit()
# print(itens)

i=0
for _ in range(1):
    wait = WebDriverWait(driver, 10)  # espera até 10 segundos
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
    )
    itens = driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item") and contains(@role, "listitem")]')
    print(len(itens))
    listaLivros = []
    for item in itens:
        if item.get_attribute("data-asin") != '':
            i+=1
            # print("ASIN:", item.get_attribute("data-asin"))
            
            print(f'\nItem {i}\n')
            
            try:
                element = item.find_element(By.CLASS_NAME, 'a-link-normal')
                link = element.get_attribute('href')
                driver.execute_script(f"window.open('{link}', '_blank');")

                print(f'Link = {link}')
                time.sleep(1)

                # Muda para a nova aba (última)
                driver.switch_to.window(driver.window_handles[-1])

                # Espera e extrai algo da página do produto
                # time.sleep(2)
                # print("Título da página:", driver.title)
                
                try:
                    # Espera até 10 segundos pelo botão com texto "Continuar comprando"
                    botao = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((
                            By.XPATH, "//button[contains(text(), 'Continuar comprando')]"
                        ))
                    )
                    botao.click()
                    print("Botão 'Continuar comprando' clicado com sucesso!")
                except:
                    print("Botão 'Continuar comprando' não encontrado.")

                # time.sleep(2)

                
                nome = driver.find_element(By.XPATH, "//span[@id='productTitle']").text
                print(f'Nome: {nome}')
                


                try:
                    element = driver.find_element(By.ID, 'bylineInfo')
                    element = element.find_element(By.XPATH, "//span[@class='author notFaded']")
                    autor = element.find_element(By.CLASS_NAME, 'a-link-normal').text
                    print(f'Autor = {autor}')
                except:
                    print('Problema no autor')
                    break
                
                try:
                    avaliacao = driver.find_element(By.ID, 'averageCustomerReviews').find_element(By.CLASS_NAME, 'reviewCountTextLinkedHistogram').get_attribute('title')
                except:
                    avaliacao = 'Sem avaliações'
                print(f'Avaliação = {avaliacao}')

                try:
                    qtdAvaliacoes = driver.find_element(By.ID, 'acrCustomerReviewText').text
                except:
                    qtdAvaliacoes = 'Sem Avaliações'
                print(qtdAvaliacoes)

                try:
                    element = driver.find_element(By.ID, 'bookDescription_feature_div')
                    botao_mostrar_mais = WebDriverWait(element, 5).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "a-expander-prompt"))
                    )
                    botao_mostrar_mais.click()
                except:
                    print("Não há botão de expandir ou já está expandido.")

                descricao = driver.find_element(By.ID, 'bookDescription_feature_div').find_element(By.CLASS_NAME, 'a-expander-content').text

                print(f'Descricao = {descricao}')

                try:
                    element = driver.find_element(By.XPATH, "//div[@id='rich_product_information-learn_more_section']")
                    element = element.find_element(By.XPATH, "//a[@id='rich_product_information-learn_more_link']")
                    element.click()
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@id="detailBulletsWrapper_feature_div"]'))
                    )
                    element = element.find_element(By.XPATH, "//div[@id='detailBullets_feature_div']")
                    elements = element.find_elements(By.CLASS_NAME, 'a-list-item')
                    sucesso = True
                except:
                    sucesso = False
                    pass
                categoria = 'Sem categoria'
                if sucesso:
                    for element in elements:
                        if "Ranking" in element.text:
                            categoria = element.text

                print(f'Categoria = {categoria}')

                # Fecha a aba atual
                driver.close()

                # Volta para a aba anterior (lista de produtos)
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                livro = Livro(nome, descricao, autor, avaliacao, qtdAvaliacoes, categoria, link)
                listaLivros.append(livro)
            except Exception as e:
                print("Erro:", e)

    pdfBuilder.adicionarLivros(listaLivros)
    try:
        element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[class*='s-pagination-container']")
        ))
        # element = driver.find_element(By.CSS_SELECTOR, "div[class*='s-pagination-container']")
        element = element.find_element(By.CSS_SELECTOR, "span[class*='s-pagination-strip']")
        element = element.find_element(By.CSS_SELECTOR, "a[class*='s-pagination-next']")
        element.click()
    except:
        pass
pdfBuilder.encerrarDocumento()
