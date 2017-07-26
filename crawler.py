import MySQLdb
import requests

from Queue import Queue
from bs4 import BeautifulSoup
from imdb import imdb,IMDbError,IMDbDataAccessError
from movie import Movie
from threading import Thread

## We use multi-thread to crawl the data
thread_number = 5

## Below are variables associated with IMDB data
imdb_new_movie_url='http://www.imdb.com/movies-coming-soon/'
imdb_access = imdb.IMDb()

# the multi-processor queue of movie IDs
movie_IDs = Queue(maxsize = 500)
movies = Queue(maxsize = 500)

# the time range where we search for movies
begin_year = 2017
end_year = 2017

begin_month = 7
end_month = 7

## Below are variables associated with database
use_db = True

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = '112358'
mysql_db = 'mv'

def get_IDs():
    '''
    Get the movie IDs by crawling the IMDB website. We will later use these
    IDs to get more information about the movie using IMDbPy.
    '''
    for year, month in zip(range(begin_year, end_year+1), range(begin_month, end_month+1)):
        url = imdb_new_movie_url + ( '%d-%02d' % (year, month) )

        print " - GET_ID - movie url: ", url

        soup = BeautifulSoup(requests.get(url).content, "lxml")

        list_item = soup.findAll(True, {'class': "list_item"})
        for item in list_item:
            h4 = item.findAll('h4')
            for h in h4:
                m_id = h.find('a').get('href')
                m_id = m_id[9: m_id.index('?')-1]
                movie_IDs.put(m_id)
                print " - GET_ID - movie ID: ", m_id

def get_info():
    while True:
        try:
            m_id = movie_IDs.get()
            movie = imdb_access.get_movie(m_id)
            new_movie = Movie()
            new_movie.id = m_id
            new_movie.title = movie.get('title')
            movies.put(new_movie)
            movie_IDs.task_done()
        except IMDbDataAccessError:
            print ' - GET_INFO - An {} exception occured'.format(e)
            sleep(2)

def store_movies():
    conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
    cur = conn.cursor()
    while True:
        try:
            new_movie = movies.get()
            cur.execute(
                "INSERT INTO new_movies values(%s, %s)",
                (new_movie.id, new_movie.title)
            )
            conn.commit()
            print 'insert movie(ID: %s, title: %s) success.' % (new_movie.id, new_movie.title)
            movies.task_done()
        except Exception as e:
            print 'db_thread: An {} exception occured'.format(e)
    conn.close()

def thread_init():
    for i in range(thread_number):
        if i == thread_number-1 and use_db:
            t = Thread(target=store_movies)
        else:
            t=Thread(target=get_info)
        t.deamon = True
        t.start()

if __name__ == '__main__':
    thread_init()
    get_IDs()

    movie_IDs.join()
    movies.join()
    print 'Done crawling data from IMDB!'
