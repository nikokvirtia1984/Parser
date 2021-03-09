import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cars.csv'
HOST = 'https://ap.ge/ge'
URL = 'https://ap.ge/ge/search?utf8=%E2%9C%93&short_form=0&s%5Bbrand_id%5D=8&s%5Byear_from%5D=0&s%5Bprice_from%5D=&s' \
      '%5Bcountry_id%5D=0&s%5Bengine_type%5D%5B%5D=0&s%5Blegal_status%5D%5B%5D=&s%5Bmodel_id%5D=0&s%5Byear_to%5D=0&s' \
      '%5Bprice_to%5D=&s%5Bcity_id%5D=0&s%5Bgearbox%5D%5B%5D=0 '
HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                                                       'Win64; x64) '
                                                                                       'AppleWebKit/537.36 (KHTML, '
                                                                                       'like Gecko) '
                                                                                       'Chrome/88.0.4324.190 '
                                                                                       'Safari/537.36'}


def get_html(url, params=''):  # params- საიტის პარამეტრები..
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='infoCatalog')
    cars = []

    for item in items:
        cars.append(
            {
                'Overview': item.find('div', class_='paramCatalog').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='titleCatalog').find('a').get('href'),
                'Mark': item.find('div', class_='titleCatalog').get_text(strip=True),
                'Price': item.find('div', class_='priceCatalog').get_text(strip=True)
            }
        )
    return cars


def save_data(items, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Overview', 'Product link', 'Mark', 'Price'])
        for item in items:
            writer.writerow([item['Overview'], item['link_product'], item['Mark'], item['Price']])


def parser():
    PAGENATION = input('Enter number of pages for parsing: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        for page in range(1, PAGENATION):
            if PAGENATION >= 101:
                print('Maximum number of pages are 100')
                exit()
            else:
                print(f'parsing page: {page}')
                html = get_html(URL, params={'page': page})
                cars.extend(get_content(html.text))
                save_data(cars, CSV)
        pass

    else:
        print('Error')


parser()
