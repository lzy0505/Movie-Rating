import requests
import time
import logging
import pymysql
from queue import Queue
from bs4 import BeautifulSoup
from movie import Movie
from threading import Thread



# Below are variables associated with IMDB data
imdb_new_movie_url = 'http://www.imdb.com/movies-coming-soon/'
crews = ['directors','writers','producers','composers','cinematographers','editors','art_directors','costume_designers']  



# the multi-processor queue of movie IDs
mvIDQ = Queue(maxsize=200)
mvINQ = Queue(maxsize=200)



def get_IDs(year,month):
    '''
    Get the movie IDs by crawling the IMDB website. We will later use these
    IDs to get more information about the movie using IMDbPy.
    ''' 
    if month==1:
        year-=1
        month =12
    url = imdb_new_movie_url + ('%d-%02d' % (year, month))
    # decode the webpage using BeautifulSoup
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    list_item = soup.findAll(True, {'class': "list_item"})
    for item in list_item:
        h4 = item.findAll('h4')
        for h in h4:
            m_id = h.find('a').get('href')
            m_id = m_id[9: m_id.index('?')-1]
            # put id into queue
            mvIDQ.put(m_id)
    logging.info('-CRAWLER- Finished on getting movie id.')


def get_rating(mvID):
    url = "http://www.imdb.com/title/tt%s/ratings?ref_=tt_ov_rt"% mvID
    soup = BeautifulSoup(requests.get(url).content,"lxml")
    lVoting=soup.body.find('div',id='wrapper').find('div',id='root').find('div',id='pagecontent').find('div',id='content-2-wide').find('div',id='main').section.find('div',class_='title-ratings-sub-page').table.find_all('div',class_="leftAligned")
    lIntVoting=[]
    for i in range(1,len(lVoting)):
        lIntVoting.append(int(lVoting[i].string.replace(",", "")))
    return lIntVoting


def get_movie(id):
    mv = Movie()
    mv.id = id
    url = 'http://www.imdb.com/title/tt%s/reference' % id
    soup = BeautifulSoup(requests.get(url).content, "lxml")
# Title & Year
    tt=soup.head.title.string
    length=len(tt)
    title=tt[0:length-31]
    mv.title=title
    year = tt[length-29:length-25]
    mv.year= year

# Posters
    cover_url=soup.body.find(class_="titlereference-primary-image")['src']
    giant_cover_url=cover_url[0:cover_url.index('@._')+1]+'._V1_SY1000_CR0,0,675,1000_AL_.jpg'
    cover_url=cover_url[0:cover_url.index('@._')+1]+'._V1_SY270_CR0,0,180,270_.jpg'
    mv.cover_url=cover_url
    mv.giant_cover_url=giant_cover_url


# Crews
    lists=''
    for keyword in crews:   
        lists=''
        get=soup.body.find(id=keyword)
        if get is None:
            mv.crews[keyword]='NULL'
        else:
            for item in get.parent.parent.next_sibling.next_sibling.find_all(class_='name'):
                lists+=item.a.string+"$"
            mv.crews[keyword]=lists.rstrip("$")



# Casts
    lists=[]
    for item in soup.body.find(class_='cast_list').find_all(itemprop="actor"):
        actor=[]
        actor.append(item.a.span.string)
        actor.append(item.a['href'][8:15])
        lists.append(actor)
    while len(lists) <3:
        lists.append(['NULL','0000000'])
    mv.casts=lists



# Runtime
    content=[]
    details = soup.body.find(class_="titlereference-section-additional-details")
    content_list = details.find(text='Runtime').parent.next_sibling.next_sibling.ul
    for item in content_list.find_all('li'):
        t=item.string.lstrip().rstrip()
        content.append(t[0:len(t)-4])
    mv.runtimes=content[0]

# Country
    content_list = details.find(text='Country').parent.next_sibling.next_sibling.ul
    content=''
    for item in content_list.find_all('li'):
        content+=item.a.string+'$'
    mv.countries=content.rstrip("$")

# Language
    content_list = details.find(text='Language').parent.next_sibling.next_sibling.ul
    content=''
    for item in content_list.find_all('li'):
        content+=item.a.string+'$'
    mv.languages=content.rstrip("$")

# Color
    content_list = details.find(text='Color').parent.next_sibling.next_sibling.ul
    content=''
    for item in content_list.find_all('li'):
        content+=item.a.string+'$'
    mv.color_info=content.rstrip("$")


# Genres
    genres = soup.body.find(class_="titlereference-section-storyline")
    content_list = genres.find(text='Genres').parent.next_sibling.next_sibling.ul
    content=''
    for item in content_list.find_all('li'):
        content+=item.a.string+'$'
    mv.genres = content.rstrip("$")


# Production companies
    companies = soup.body.find(class_="ipl-header__content ipl-list-title",text='Production Companies')
    if companies is None:
        content='NULL'
    else:
        content_list = companies.parent.parent.next_sibling.next_sibling
        content=''
        for item in content_list.find_all('li'):
            content+=item.a.string+'$'
    mv.production_companies= content.rstrip("$")


#Ratings
    mv.number_of_votes = get_rating(id)

    return mv


def get_info():
    logging.info("-CRAWLER- Start to get movie feature...")
    while not mvIDQ.empty():
        try:
            mvID = mvIDQ.get()
            mvOJ = get_movie(mvID)
            mvINQ.put(mvOJ)
            mvIDQ.task_done()
        except Exception as e:
            logging.exception('-CRAWLER- An {} exception occured at get_info()!'.format(e), mvID)
        time.sleep(1)
    logging.info('-CRAWLER- Finished on getting movie features.')
        

def store_movies():
    time.sleep(20)
    logging.info("-CRAWLER- Start to store movie feature...")
    conn = pymysql.connect(host='movie-data.ch6y02vfazod.ap-northeast-1.rds.amazonaws.com',
                             user='admin',
                             password='********',
                             database='movierating',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        while not mvINQ.empty():
            try:
                mvIN = mvINQ.get()
                ssum = 0.0
                rating = []
                for n in mvIN.number_of_votes:
                    ssum += n
                    rating.append(n)
                for i in range(len(rating)):
                    rating[i] = rating[i]/ssum

                cursor.execute(
                    "INSERT INTO `data` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    ('test',
                        mvIN.id,
                        mvIN.title,
                        mvIN.cover_url,
                        mvIN.giant_cover_url,
                        mvIN.genres,
                        mvIN.color_info,
                        mvIN.casts[0][0],
                        # mvIN.casts[0][2],#ranking
                        '1',
                        mvIN.casts[1][0],
                        '2',
                        # mvIN.casts[1][2],
                        mvIN.casts[2][0],
                        '3',
                        # mvIN.casts[2][2],
                        mvIN.countries,
                        mvIN.languages,
                        mvIN.crews['directors'],
                        mvIN.crews['writers'],
                        mvIN.crews['producers'],
                        mvIN.crews['composers'],
                        mvIN.crews['cinematographers'],
                        mvIN.crews['editors'],
                        mvIN.crews['art_directors'],
                        mvIN.crews['costume_designers'],
                        mvIN.production_companies,
                        mvIN.year,
                        mvIN.runtimes,
                        '10.0',
                        rating[0],
                        rating[1],
                        rating[2],
                        rating[3],
                        rating[4],
                        rating[5],
                        rating[6],
                        rating[7],
                        rating[8],
                        rating[9],
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0',
                        '0.0'))
                logging.info('-CRAWLER- Store moive(ID: %s) successfully.(Remain %d)' % (mvIN.id,mvIDQ.qsize()+mvINQ.qsize()))
                conn.commit()
                mvINQ.task_done()
            except Exception as e:
                logging.exception('-CRAWLER- An {} exception occured at store_movies()!'.format(e))
    conn.close()
    logging.info("-CRAWLER- Finished on store movie feature...")

def thread_init():
    for i in range(thread_number):
        if i == thread_number-1:
            t = Thread(target=)
        else:
            t = Thread(target=) 
        t.deamon = True
        t.start()


def run():
    year=time.localtime(time.time())[0]
    month=time.localtime(time.time())[1]
    get_IDs(year,month)
    get_info()
    mvIDQ.join()
    store_movies()
    mvINQ.join()
    logging.info("Finnish ALL tasks!")

if __name__ == '__main__':
    run()


    
