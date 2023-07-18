import requests
import csv
from bs4 import BeautifulSoup as bs

def write_to_csv(data):
    with open('dannye.csv', 'a') as file:
        writer = csv.writer(file,delimiter='\n')
        writer.writerow([data['title'], data['pricebucks'],   data['description'] ,  data['image']])

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('ul', class_="pagination").find_all('a')[-1].attrs.get('data-page')
    if page_list is not None:
        return int(page_list)
    else:
        return 0

def get_data(html):
    soup = bs(html, 'lxml')
    carlist = soup.find('div', class_ = 'table-view-list').find_all('div', class_ = 'list-item list-label')

    for cars in carlist:
        try:
            title = cars.find('div',class_ = "block title").find('h2').text.strip()
        except AttributeError:
            title = ''
        try:
            pricebucks = cars.find('div', class_ = 'price').find('strong').text.split()
            pricebucks = ' '.join(pricebucks)
        except AttributeError:
            pricebucks = ''
        try:
            image = cars.find('div', class_ = 'thumb-item-carousel').find('img').attrs.get('data-src')
        except:
            image = ''
        try:
            description = cars.find('div', class_ = 'block info-wrapper item-info-wrapper').text.split()
            description = ''.join(description)
        except AttributeError:
            description = ''
        product_dict = {'title': title, 'pricebucks' : pricebucks,  'image' : image, 'description' : description}
        write_to_csv(product_dict)

def main():
    url = 'https://www.mashina.kg/search/all/'
    html = get_html(url)
    get_data(html)
    number = get_total_pages(html)
    for i in range(1, number + 1):
        url_with_page = url + '&page=' + str(i)
        html = get_html(url_with_page)
        get_data(html)
        print(f'Спарсили -{i} страницу')

with open('dannye.csv', 'w') as file:
   write_ = csv.writer(file)
   write_.writerow(['title' , 'pricebucks' ,  'image' , 'description'])




main()