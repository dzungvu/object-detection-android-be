from django.shortcuts import render
import requests
from django.http import JsonResponse
from bs4 import BeautifulSoup
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Create your views here.

DEBUG_FOLDER = 'debug'
LOG_FILE_FOLDER = "log_file"

def is_folder_exist(path):
        return os.path.exists(path)

def create_folder_if_not_exist(folder_path):
        if not is_folder_exist(path=folder_path):
            os.makedirs(folder_path)
            print(f'Folder {folder_path} created.')
        else:
            print(f'Folder {folder_path} already existed.')

def write_debug_file(file_name, content):
    debug_log_file_path = os.path.join(DEBUG_FOLDER, LOG_FILE_FOLDER)
    create_folder_if_not_exist(debug_log_file_path)
    raw_data_file = os.path.join(debug_log_file_path, file_name)
    with open(raw_data_file, 'w', encoding='utf-8') as file:
        file.write(content)
        file.close()


def search_shop(request):
    

    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    search_url = f"https://www.google.com/search?q={query}&tbm=shop"
    print('Running search on:', search_url)
    # search_url = f"https://9gag.com/"


    # current_path = os.path.dirname(os.path.abspath(__file__))
    # CHROME_DRIVER_PATH = os.path.join(current_path, 'chromedriver-mac-arm64', 'chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for some server environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    # service = Service(CHROME_DRIVER_PATH)
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor

    response = driver.get(url=search_url)
    response_source = driver.page_source

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    
    # response = requests.get(search_url, headers=headers)

    
    print('Search successful')
    write_debug_file('search_results.html', response_source)
    soup = BeautifulSoup(response_source, 'html.parser')
    search_results = []

    search_soup_container = soup.find('div', class_='sh-pr__product-results-grid sh-pr__product-results')
    write_debug_file('search_results_container.html', str(search_soup_container))
    if search_soup_container:
        for product_container in search_soup_container.find_all('div', class_='sh-dgr__content'):
            product_image_url_container = product_container.find('div', class_='ArOc1c')
            product_info_container = product_container.find('span', class_='C7Lkve')
            product_price_container = product_container.find('div', class_='sh-dgr__offer-content')
            product_url = product_container.find('a', class_='xCpuod')['href']
            product_url = product_url.replace(u"/url?url=", "")  # Replace "url?url=" with an empty string

            search_results.append({
                'title': product_info_container.find('h3', class_='tAxDx').get_text(),
                'price': product_price_container.find('span', class_=u'a8Pemb OFFNJ').get_text(),
                'product_url': product_url,
                'image_url': product_image_url_container.find('img')['src']
            })
    else:
        print('No search results found')
    
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        search_results.append(g.get_text())
    
    return JsonResponse({'results': search_results})


# Create a request interceptor
def interceptor(request):
    del request.headers['User-Agent']  # Delete the header first
    request.headers['User-Agent'] = 'Mozilla/5.0'