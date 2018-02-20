import requests
import time
import sqlite3
from queue import Queue
from bs4 import BeautifulSoup
from movie import Movie
from threading import Thread

# the time range where we search for movies
begin_year = 2015
end_year = 2015
begin_month = 7
end_month = 8

# train or test
mode = 'test'



# We use multi-thread to crawl the data
thread_number = 9

# Below are variables associated with IMDB data
imdb_new_movie_url = 'http://www.imdb.com/movies-coming-soon/'
crews = ['directors','writers','producers','composers','cinematographers','editors','art_directors','costume_designers']  



# the multi-processor queue of movie IDs
mvIDQ = Queue(maxsize=500)
mvINQ = Queue(maxsize=100)

stage = 0


def get_IDs():
    '''
    Get the movie IDs by crawling the IMDB website. We will later use these
    IDs to get more information about the movie using IMDbPy.
    '''
    global stage
    for year in range(begin_year, end_year+1):
        for month in range(1, 12+1):
            if(year == begin_year and month < begin_month):
                continue
            elif(year == end_year and month >= end_month):
                break
            else:
                url = imdb_new_movie_url + ('%d-%02d' % (year, month))
                print ("-CRAWLER- Getting movie id from: %s" % url)
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
                        print ("-CRAWLER- Got movie id: %s" % m_id)
    stage = 1
    print ('-CRAWLER- Finished on getting movie id.')


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
    giant_cover_url=cover_url[0:cover_url.index('@')+1]+'._V1_SY1000_CR0,0,675,1000_AL_.jpg'
    cover_url=cover_url[0:cover_url.index('@')+1]+'._V1_SY300_CR0,0,200,300_.jpg'
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
    global stage
    time.sleep(5)
    print ("-CRAWLER- Start to get movie feature...")
    while (not mvIDQ.empty()) or stage == 0:
        try:
            mvID = mvIDQ.get()
            # print "-CRAWLER- Getting movie(id: %s) feature..." % mvID
            mvOJ = get_movie(mvID)
            mvINQ.put(mvOJ)
            mvIDQ.task_done()
            # print '-CRAWLER- Get movie features(ID: %s) successfully.' % mvID
        except Exception as e:
            print ('-CRAWLER- An {} exception occured!'.format(e), mvID)
            mvINQ.put(mvID)
        time.sleep(1)
    stage = 2
    print ("Done!")
    print ('-CRAWLER- Finished on getting movie features.')
        

def store_movies():
    global stage
    time.sleep(20)
    print ("-CRAWLER- Start to store movie feature...")
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    while (not mvINQ.empty()) or stage < 2:
        try:
            mvIN = mvINQ.get()
            cur.execute(
                "INSERT INTO feature values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (mode,
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
                    mvIN.runtimes))
            ssum = 0.0
            rating = []
            for n in mvIN.number_of_votes:
                ssum += n
                rating.append(n)
            for i in range(len(rating)):
                rating[i] = rating[i]/ssum

            cur.execute(
                "INSERT INTO rating values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (mvIN.id, 
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
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL",
                    "NULL"))
            print ('-CRAWLER- Store moive(ID: %s) successfully.(Remain %d)' % (mvIN.id,mvIDQ.qsize()+mvINQ.qsize()))
            conn.commit()
            mvINQ.task_done()
        except Exception as e:
            print ('-CRAWLER- An {} exception occured at store_movies()!'.format(e))
    conn.close()
    print ("-CRAWLER- Finished on store movie feature...")

def thread_init():
    for i in range(thread_number):
        if i == thread_number-1:
            t = Thread(target=store_movies)
        else:
            t = Thread(target=get_info) 
        t.deamon = True
        t.start()

if __name__ == '__main__':
    thread_init()
    get_IDs()
    mvIDQ.join()
    mvINQ.join()
    print ("Finnish ALL!")


    
