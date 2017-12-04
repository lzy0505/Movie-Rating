import requests
import time
import sqlite3
from Queue import Queue
from bs4 import BeautifulSoup
from imdb import imdb
from movie import Movie
from threading import Thread

# the time range where we search for movies
begin_year = 2015
end_year = 2015
begin_month = 7
end_month = 9

# train or test
mode = 'test'



# We use multi-thread to crawl the data
thread_number = 9

# Below are variables associated with IMDB data
imdb_new_movie_url = 'http://www.imdb.com/movies-coming-soon/'
imdb_access = imdb.IMDb()

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
                print "-CRAWLER- Getting movie id from: %s" % url
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
                        # print "-CRAWLER- Got movie id: %s" % m_id
    stage = 1
    print '-CRAWLER- Finished on getting movie id.'


def get_rating(mvID):
    url = "http://www.imdb.com/title/tt%s/ratings?ref_=tt_ov_rt"% mvID
    soup = BeautifulSoup(requests.get(url).content,"lxml")
    lVoting=soup.body.find('div',id='wrapper').find('div',id='root').find('div',id='pagecontent').find('div',id='content-2-wide').find('div',id='main').section.find('div',class_='title-ratings-sub-page').table.find_all('div',class_="leftAligned")
    lIntVoting=[]
    for i in xrange(1,len(lVoting)):
        lIntVoting.append(int(lVoting[i].string.replace(",", "")))
    return lIntVoting


def get_ranking(castid):
    casturl = 'http://www.imdb.com/name/nm'+castid
    soup = BeautifulSoup(requests.get(casturl).content,"lxml") 
    toprank=soup.body.find('div',id='wrapper').find('div',id='root').find('div',id='pagecontent').find('div',id='content-2-wide').find('div',id='meterHeaderBox').find('a')
    toprank=str(toprank)
    toprank=toprank[toprank.index('>')+1:len(toprank)-4]
    if(toprank.isalnum()==True):
        ranking=int(toprank)
        if(ranking<=50):
            toprank='Top50' #if rank <=50 cluster TOP 50 
        else:
            toprank='Top500'
        if(ranking<=5):
            toprank='Top5' #if rank <=5 cluster TOP 5
    if(toprank=='SEE RANK'):
        toprank='5000+'
    toprank=toprank.replace(' ','')
    return toprank



def get_info():
    global stage
    time.sleep(5)
    print "-CRAWLER- Start to get movie feature..."
    while (not mvIDQ.empty()) or stage == 0:
        try:
            mvID = mvIDQ.get()
            # get info from imdmpy with movie id
            # print "-CRAWLER- Getting movie(id: %s) feature..." % mvID
            mvIN = imdb_access.get_movie(mvID)
            # create new Movie object
            mvOJ = Movie()
            # ID string
            mvOJ.id = mvID
            # title string
            mvOJ.title = mvIN.get('title')
            # poster url string
            mvOJ.cover_url = mvIN.get('cover url')
            # Bigger poster url string
            mvOJ.giant_cover_url = mvIN.get('full-size cover url')
            # genres string list
            if mvIN.has_key('genres'):
                sIN = ""
                for i in mvIN.get('genres'):
                    sIN += (i + '$')
                mvOJ.genres = sIN[0:len(sIN)-1]
            # color string list
            if mvIN.has_key('color info'):
                sIN = ""
                for i in mvIN.get('color info'):
                    sIN += (i + '$')
                mvOJ.color_info = sIN[0:len(sIN)-1]
            # director string list
            if mvIN.has_key('director'):
                sIN = ""
                for i in mvIN.get('director'):
                    sIN += i['name']+'$'
                mvOJ.director = sIN[0:len(sIN)-1] 
            # 1st Actor
            mvOJ.cast_1st = mvIN.get('cast')[0]['name']
            # TODO 
            mvOJ.cast_1st_rank = get_ranking(mvIN.get('cast')[0].getID())
            if len(mvIN.get('cast')) >= 2:
                # 2nd Actor
                mvOJ.cast_2nd = mvIN.get('cast')[1]['name']
                mvOJ.cast_2nd_rank = get_ranking(mvIN.get('cast')[1].getID())
            if len(mvIN.get('cast')) >= 3:
                # 3rd Actor
                mvOJ.cast_3rd = mvIN.get('cast')[2]['name']
                mvOJ.cast_3rd_rank = get_ranking(mvIN.get('cast')[2].getID())
            # country string list
            if mvIN.has_key('countries'):
                sIN = ""
                for i in mvIN.get('countries'):
                    sIN += (i + '$')
                mvOJ.countries = sIN[0:len(sIN)-1]
            # language string list
            if mvIN.has_key('languages'):
                sIN = ""
                for i in mvIN.get('languages'):
                    sIN += (i + '$')
                mvOJ.languages = sIN[0:len(sIN)-1]
            # writer string list
            if mvIN.has_key('writer'):
                sIN = ""
                for i in mvIN.get('writer'):
                    sIN += i['name']+'$'
                mvOJ.writer = sIN[0:len(sIN)-1]
            # editor string list
            if mvIN.has_key('editor'):
                sIN = ""
                for i in mvIN.get('editor'):
                    sIN += i['name']+'$'
                mvOJ.editor = sIN[0:len(sIN)-1]
            # cinematographer string list
            if mvIN.has_key('cinematographer'):
                sIN = ""
                for i in mvIN.get('cinematographer'):
                    sIN += i['name']+'$'
                mvOJ.cinematographer = sIN[0:len(sIN)-1]
            # art direction string list
            if mvIN.has_key('art direction'):
                sIN = ""
                for i in mvIN.get('art direction'):
                    sIN += i['name']+'$'
                mvOJ.art_director = sIN[0:len(sIN)-1]
            # costume designer string list
            if mvIN.has_key('costume designer'):
                sIN = ""
                for i in mvIN.get('costume designer'):
                    sIN += i['name']+'$'
                mvOJ.costume_designer = sIN[0:len(sIN)-1]
            # music By string list
            if mvIN.has_key('original music'):
                sIN = ""
                for i in mvIN.get('original music'):
                    sIN += i['name']+'$'
                mvOJ.original_music = sIN[0:len(sIN)-1]
            # sound string list
            if mvIN.has_key('sound mix'):
                sIN = ""
                for i in mvIN.get('sound mix'):
                    sIN += (i + '$')
                mvOJ.sound_mix = sIN[0:len(sIN)-1]
            # production company string list
            if mvIN.has_key('production companies'):
                sIN = ""
                for i in mvIN.get('production companies'):
                    sIN += i['name']+'$'
                mvOJ.production_companies = sIN[0:len(sIN)-1]
            # year int
            if mvIN.has_key('year'):
                mvOJ.year = mvIN.get('year')
            else:
                mvOJ.year = 0
            # running time int
            if mvIN.has_key('runtimes'):
                try:
                    if str(mvIN.get('runtimes')[0]).find(':') != -1:
                            mvOJ.runtimes = int(str(mvIN.get('runtimes')[0]).split(':')[1])
                    else:
                        mvOJ.runtimes = int(mvIN.get('runtimes')[0])
                except Exception:
                    mvOJ.runtimes = 0
            else:
                mvOJ.runtimes = 0
            mvOJ.number_of_votes = get_rating(mvID)
            mvINQ.put(mvOJ)
            mvIDQ.task_done()
            # print '-CRAWLER- Get movie features(ID: %s) successfully.' % mvID
        # TODO cannot handle exception
        except Exception, e:
            print '-CRAWLER- An {} exception occured!'.format(e), mvID
            mvINQ.put(mvID)
        time.sleep(1)
    stage = 2
    print "Done!"
    print '-CRAWLER- Finished on getting movie features.'
        

def store_movies():
    global stage
    time.sleep(20)
    print "-CRAWLER- Start to store movie feature..."
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
                    mvIN.director,
                    mvIN.cast_1st,
                    mvIN.cast_1st_rank,
                    mvIN.cast_2nd,
                    mvIN.cast_2nd_rank,
                    mvIN.cast_3rd,
                    mvIN.cast_3rd_rank,
                    mvIN.countries,
                    mvIN.languages,
                    mvIN.writer,
                    mvIN.editor,
                    mvIN.cinematographer,
                    mvIN.art_director,
                    mvIN.costume_designer,
                    mvIN.original_music,
                    mvIN.sound_mix,
                    mvIN.production_companies,
                    mvIN.year,
                    mvIN.runtimes))
            ssum = 0.0
            rating = []
            for n in mvIN.number_of_votes:
                ssum += n
                rating.append(n)
            for i in xrange(0, len(rating)):
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
            print '-CRAWLER- Store moive(ID: %s) successfully.(Remain %d)' % (mvIN.id,mvIDQ.qsize()+mvINQ.qsize())
            conn.commit()
            mvINQ.task_done()
        except Exception, e:
            print '-CRAWLER- An {} exception occured at store_movies()!'.format(e)
    conn.close()
    print "-CRAWLER- Finished on store movie feature..."


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
    print "Finnish ALL!"

    
