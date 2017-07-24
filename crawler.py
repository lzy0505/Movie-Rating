from imdb import imdb,IMDbError,IMDbDataAccessError
from bs4 import BeautifulSoup
import requests
from Queue import Queue
from threading import Thread

thread_number = 5

## Below are constants associated with IMDB data
imdb_new_movie_url='http://www.imdb.com/movies-coming-soon/'
imdb_access = imdb.IMDb()

# the multi-processor queue of movie IDs
movieID = Queue(maxsize = 500)

# the time range where we search for movies
begin_year = 2017
end_year =2017

begin_month = 7
end_month =7

def get_ID():
    for year, month in zip(range(begin_year, end_year+1), range(begin_month, end_month+1)):
        url=imdb_new_movie_url + ( '%d-%02d' % (year, month) )

        print " - GET_ID - movie url: ", url

        soup=BeautifulSoup(requests.get(url).content, "lxml")

        list_item = soup.findAll(True, {'class': "list_item"})
        for item in list_item:
            h4 = item.findAll('h4')
            for h in h4:
                link = h.find('a').get('href')
                link = link[9: link.index('?')-1]
                movieID.put(link)
                print " - GET_ID - link: ", link

def get_Info():
    while True:
        try:
            m_id = movieID.get()
            movie= imdb_access.get_movie(m_id)
            print movie.get('title')
            movieID.task_done()
        except IOError as e:
            print ' - GET_INFO - An {} exception occured'.format(e)
            
def thread_Init():
    for i in range(thread_number):
        t=Thread(target=get_Info)
        t.start()

if __name__ == '__main__':
    thread_Init()
    get_ID()
    movieID.join()

    print 'Done crawling data from IMDB!'
