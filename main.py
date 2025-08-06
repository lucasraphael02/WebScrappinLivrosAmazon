from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")

# Cria corretamente o serviço do driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.amazon.com.br/s?k=B0FD84D3SK%7CB0DHLTHVYF%7CB0CZYN1L9Z%7CB0D24NFJTB%7CB07NNQHM86%7CB0DBTYGKRV%7CB0D96K7NQF%7CB0CXBJSP7G%7CB0C2JT5ZQ1%7CB0C7K8KMM7%7CB0BMTN1TCR%7CB07MG7KVWW%7CB0FJVMSXNZ%7CB0CR6QXQQF%7CB0CX7GL944%7CB0F3FMGZ5G%7CB0C37J95ST%7CB0C1WDQDCY%7CB0B54VMDVS%7CB0BBQCT1WR%7CB0DFVRBK6T&i=digital-text&rh=p_36%3A-1&s=review-rank&language=pt_BR&ds=v1%3A0KTyEpHNRcYg1RPLt8BRvDimYH%2BgEx9iYybDeMGLB30&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91"

MAX_TENTATIVAS = 5

sucesso = False
tentativas = 0
listaLivros = []

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

itens = driver.find_elements(By.CLASS_NAME, 's-result-item')
# print(len(itens))

# exit()
# print(itens)
i=0
for item in itens:
    if item.get_attribute("data-asin") != '':
        i+=1
        # print("ASIN:", item.get_attribute("data-asin"))
        nome = item.find_element(By.CSS_SELECTOR, 'h2[aria-label]').get_attribute('aria-label')
        print(f'\nItem {i}\n')
        print(f'Nome: {nome}')
        try:
            element = item.find_element(By.CLASS_NAME, 'a-link-normal')
            link = element.get_attribute('href')
            driver.execute_script(f"window.open('{link}', '_blank');")

            print(f'Link = {link}')
            time.sleep(1)

            # Muda para a nova aba (última)
            driver.switch_to.window(driver.window_handles[-1])

            # Espera e extrai algo da página do produto
            time.sleep(2)
            # print("Título da página:", driver.title)
            try:
                autor = driver.find_element(By.ID, 'bylineInfo_feature_div').find_element(By.CLASS_NAME, 'a-link-normal').text
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
                qtdAvaliacoes = '0'
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
            # Fecha a aba atual
            driver.close()

            # Volta para a aba anterior (lista de produtos)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        except Exception as e:
            print("Erro:", e)

# element = driver.find_element(By.CLASS_NAME, 's-pagination-container').find_element(By.CLASS_NAME, 's-pagination-next')
# element.click()
time.sleep(10)