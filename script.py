import requests
from bs4 import BeautifulSoup
import json

headers = {
    "user-agent": "",
    "accept-encoding": "",
    "accept": "",
    "accept-language": ""
}


def get_data(src):
    soup = BeautifulSoup(src, 'lxml')

    res_dict = {}
    articles = soup.find_all(class_='node-wrapper')
    for item in articles:
        if item.find(class_='trim'):
            name = item.find(class_='trim').text
        if item.find(class_='number'):
            price = item.find(class_='number').text

        res_dict[name] = price

    print(res_dict)
    return res_dict


def pagination(src, link):
    category_res = {}

    soup = BeautifulSoup(src, 'lxml')

    title = soup.find(class_='title').text

    if soup.find(class_='pager'):
        pager_list = soup.find(class_='pager')

        if pager_list.find_all("li"):
            pages = pager_list.find(class_="last").text
            print(pages)
            for page in range(int(pages)):
                print(page)
                adress = f'{link}?page={int(page)}'
                print(adress)
                req = requests.get(adress, headers=headers).text

                get_data(req)
                category_res[page] = get_data(req)

    with open(f'categories/{title}.json', 'w', encoding='utf-8') as f:
        json.dump(category_res, f, indent=4, ensure_ascii=False)


def categories_scrap(src):
    soup = BeautifulSoup(src, 'lxml')

    field_content = soup.find_all('div', class_='field-content')

    for item in field_content:
        link = 'https://newtea.ua/' + item.find('a')['href']
        print(link)
        req = requests.get(link, headers=headers)
        pagination(req.text, link)


test = requests.get('https://newtea.ua/chay', headers=headers)
categories_scrap(test.text)
