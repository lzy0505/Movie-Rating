from imdb import imdb,IMDbError,IMDbDataAccessError
from bs4 import BeautifulSoup
import requests
from Queue import Queue
from threading import Thread


movieID = Queue(maxsize = 500)


# thread_number = 5
# threads=[]


imdb_new_movie_url='http://www.imdb.com/movies-coming-soon/'

begin_year = 2017
begin_month = 7
end_year =2017
end_month =7




def get_ID():
    month=begin_month
    year=begin_year
    while True:
        data_string = '%d-%02d' % (year, month)
        url=imdb_new_movie_url + data_string
        print "getting movieID from: "+url
        soup=BeautifulSoup(requests.get(url).content,"lxml")
        list_item = soup.findAll(True, {'class': "list_item"})
        for item in list_item:
            h4 = item.findAll('h4')
            for h in h4:
                link = h.find('a').get('href')
                link = link[9: link.index('?')-1]
                print link
                movieID.put(link)
        if month==end_month and year==end_year:
            break
        if month==12:
            month=1
            year=year+1
        else:
            month=month+1




def get_Info():
    imdb_access = imdb.IMDb()
    while True:
        try:
            if movieID.empty():
                break
            else:
                m_movieID=movieID.get()
                movie= imdb_access.get_movie(m_movieID)
                print movie.get('title')   
                movieID.task_done()  
        except IOError as err:
            movieID.put(m_movieID)
            print 'Access Error with'+m_movieID
            

# def thread_Init():
#     for i in range(thread_number):
#         t=Thread(target=get_Info)
#         threads.append(t)

# def thread_Start():
#     for i in range(thread_number):
#         threads[i].start()


if __name__ == '__main__':
    #thread_Init()
    get_ID()
    get_Info()
    #thread_Start()
    #movieID.join()
    print 'DONE!'
