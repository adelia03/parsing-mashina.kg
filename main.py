import requests, csv
from bs4 import BeautifulSoup as BS

main_url = 'https://www.mashina.kg/search/?currency=2&price_from=&price_to=&page=1'

def get_soup(url: str) -> BS:
    # headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    # import time
    # time.sleep(5)
    response = requests.get(url)
    return BS(response.text, 'lxml')


def get_all(soup):
    for product in soup.find_all('div', {'class':'list-item list-label'}):
        try:
            image = product.find('a').find('img').get('data-src')
        except:
            image = ''

        try:
            title = product.find('div', {'class':'block title'}).text.strip()
        except:
            title = ''

        try:
            price = product.find('div', {'class':'block price'}).find('p').text.replace(' ','').replace('\n', ' ').strip().replace('  ',' ')
        except:
            price = ''

        try:
            description = product.find('div', {'class':'block info-wrapper item-info-wrapper'}).text.replace('  ','').strip().replace('\n\n',' ').replace('  ',' ')
        except:
            description = ''

        data = {'title':title, 'price':price, 'description':description, 'image':image}
        write_to_csv(data)



def get_last_page(soup: BS):
    ul = soup.find('ul', {'class':'pagination'})
    if ul is None:
        return 1
    last = ul.find_all('li', {'class':'page-item'})
    last_ = last[-1].find('a').get('data-page')
    return last_


def write_to_csv(data):
    with open('mashina.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'], data['price'], data['description'], data['image']))



def main():
    for i in range(1,int(get_last_page(get_soup(main_url)))+1):
        url_with_page = main_url.replace('1',str(i))
        html = get_soup(url_with_page)
        get_all(html)
        print(url_with_page)
    

main()
