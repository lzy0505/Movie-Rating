# -*- coding:utf-8 -*-
import sqlite3
import requests
from bs4 import BeautifulSoup

def func(mvID):
    url = 'http://www.imdb.com/title/tt%s/reference' % mvID
    soup = BeautifulSoup(requests.get(url).content, "lxml")

    crews = ['directors','writers','producers','composers','cinematographers','editors','art_directors','costume_designers']  
    detailss = ['Runtime','Country','Language','Color']

    tt=soup.head.title.string
    length=len(tt)
    title=tt[0:length-31]
    print('title: %s' % title)
    year = tt[length-29:length-25]
    print('year: %s' % year)
    cover_url=soup.body.find(class_="titlereference-primary-image")['src']
    giant_cover_url=cover_url[0:cover_url.index('@')+1]+'._V1_SY1000_CR0,0,675,1000_AL_.jpg'
    cover_url=cover_url[0:cover_url.index('@')+1]+'._V1_SY300_CR0,0,200,300_.jpg'
    print('cover url: %s' % cover_url)
    print('full-size cover url: %s' % giant_cover_url)
    for keyword in crews:   
        lists=[]
        for item in soup.body.find(id=keyword).parent.parent.next_sibling.next_sibling.find_all(class_='name'):
            lists.append(item.a.string)
        print('%s: %s' % (keyword,lists))
    lists=[]
    for item in soup.body.find(class_='cast_list').find_all(itemprop="actor"):
        actor=[]
        actor.append(item.a.span.string)
        actor.append(item.a['href'][8:15])
        lists.append(actor)
    print('cast: %s' % lists)

    details = soup.body.find(class_="titlereference-section-additional-details")
    for keyword in detailss:
        content_list = details.find(text=keyword).parent.next_sibling.next_sibling.ul
        content=[]
        if keyword is 'Runtime':
            for item in content_list.find_all('li'):
                content.append(item.string.lstrip().rstrip())
        else:
            for item in content_list.find_all('li'):
                content.append(item.a.string)
        print('%s: %s' % (keyword,content))


    genres = soup.body.find(class_="titlereference-section-storyline")
    content_list = genres.find(text='Genres').parent.next_sibling.next_sibling.ul
    content=[]
    for item in content_list.find_all('li'):
        content.append(item.a.string)
    print('Genres: %s' % content)

    companies = soup.body.find(class_="ipl-header__content ipl-list-title",text='Production Companies')
    content_list = companies.parent.parent.next_sibling.next_sibling
    content=[]
    for item in content_list.find_all('li'):
        content.append(item.a.string)
    print('Production Companies: %s' % content)

# https://images-na.ssl-images-amazon.com/images/M/
# MV5BMjI0NzU4MjkxNl5BMl5BanBnXkFtZTgwMTYxMTA1NzE@._V1_SY1000_CR0,0,675,1000_AL_.jpg
# https://images-na.ssl-images-amazon.com/images/M/
# MV5BMjI0NzU4MjkxNl5BMl5BanBnXkFtZTgwMTYxMTA1NzE@._V1_SY150_CR0,0,101,150_.jpg

if __name__ == '__main__':
    func("3103166")
