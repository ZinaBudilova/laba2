from bs4 import BeautifulSoup
import requests
import re

with open('news.txt', 'w', encoding='utf-8') as file:

    for i in range(1, 240): #всего 239 страниц с новостями
        page = 'https://pochinok.admin-smolensk.ru/news/page/' + str(i) + '/'
        response = requests.get(page)
        urls = re.findall(r'<a href="(.+)">Подробнее', response.text)

        for url in urls:
            #print(url)
            article = requests.get('https://pochinok.admin-smolensk.ru' + url)
            soup = BeautifulSoup(article.text, features="html.parser")
            title = str(soup.find('title'))[7:-18] #убрали тег и надпись " - Новость" в конце
            date = re.findall(r'news.date">(.+?)\ ', article.text)[0]
            raw_text = str(soup.find('dd'))
            text = re.sub(r'<.+>', '', raw_text) #убираем теги
            text = re.sub(r'(\n){2,}', '\n', text) #убираем лишние переносы строк

            file.write('=====\n')
            file.write('https://pochinok.admin-smolensk.ru' + url + '\n')
            file.write('Администрация муниципального образования "Починковский район" Смоленской области\n')
            file.write(date + '\n')
            file.write('Автор не указан\n') #во всех новостях
            file.write(title + '\n')
            file.write(text + '\n')

#print('done')

