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
use_db = False

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = 'root'
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
            counter=0
            m_id = movie_IDs.get()
            movie = imdb_access.get_movie(m_id)
            new_movie = Movie()
            #ID string
            new_movie.id = m_id
            #Title string
            new_movie.title = movie.get('title')
            #Poster url string
            new_movie.cover_url=movie.get('cover url')
            #Genres string list
            if movie.has_key('genres'):
                counter=0
                for i in movie.get('genres'):
                    counter+=1
                    new_movie.genres+= (i +'$')
                    if counter==5:
                        break
                new_movie.genres=new_movie.genres[0:len(new_movie.genres)-1]
            #Color string list
            if movie.has_key('color info'):
                counter=0
                for i in movie.get('color info'):
                    new_movie.color_info+= (i +'$')
                    counter+=1
                    if counter==5:
                        break
                new_movie.color_info=new_movie.color_info[0:len(new_movie.color_info)-1]
            #Director string list
            if movie.has_key('director'):
                counter=0
                for i in movie.get('director'):
                    new_movie.director+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==5:
                        break
                new_movie.director=new_movie.director[0:len(new_movie.director)-1]
            #1st Actor
            new_movie.cast_1=movie.get('cast')[0]
            #2nd Actor
            new_movie.cast_2=movie.get('cast')[1]
            #3rd Actor
            new_movie.cast_3=movie.get('cast')[2]
            #Country string list
            if movie.has_key('countries'):
                counter=0
                for i in movie.get('countries'):
                    new_movie.countries+= (i +'$')
                    counter+=1
                    if counter==5:
                        break
                new_movie.countries=new_movie.countries[0:len(new_movie.countries)-1]
            #Language string list
            if movie.has_key('languages'):
                counter=0
                for i in movie.get('languages'):
                    new_movie.languages+= (i +'$')
                    counter+=1
                    if counter==5:
                        break
                new_movie.languages=new_movie.languages[0:len(new_movie.languages)-1]
            #Writer string list
            if movie.has_key('writer'):
                counter=0
                for i in movie.get('writer'):
                    new_movie.writer+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==5:
                        break
                new_movie.writer=new_movie.writer[0:len(new_movie.writer)-1]
            
            #Editor string list
            if movie.has_key('editor'):
                counter=0
                for i in movie.get('editor'):
                    new_movie.editor+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.editor=new_movie.editor[0:len(new_movie.editor)-1]
            
            #Cinematographer string list
            if movie.has_key('cinematographer'):
                counter=0
                for i in movie.get('cinematographer'):
                    new_movie.cinematographer+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.cinematographer=new_movie.cinematographer[0:len(new_movie.cinematographer)-1]
            
            #Art direction string list
            if movie.has_key('art direction'):
                counter=0
                for i in movie.get('art direction'):
                    new_movie.art_direction+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.art_direction=new_movie.art_direction[0:len(new_movie.art_direction)-1]
            
            #Costume designer string list
            if movie.has_key('costume designer'):
                counter=0
                for i in movie.get('costume designer'):
                    new_movie.costume_designer+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.costume_designer=new_movie.costume_designer[0:len(new_movie.costume_designer)-1]
            
            #Music By string list
            if movie.has_key('original music'):
                counter=0
                for i in movie.get('original music'):
                    new_movie.original_music+=i.getID()+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.original_music=new_movie.original_music[0:len(new_movie.original_music)-1]
            
            #Sound string list
            if movie.has_key('sound mix'):
                counter=0
                new_movie.sound_mix=movie.get('sound mix')
                for i in movie.get('sound mix'):
                    new_movie.sound_mix+= (i +'$')
                    counter+=1
                    if counter==3:
                        break
                new_movie.sound_mix=new_movie.sound_mix[0:len(new_movie.sound_mix)-1]
            
            #Production company string list
            if movie.has_key('production companies'):
                counter=0
                new_movie.production_companies=movie.get('production companies')
                for i in movie.get('production companies'):
                    new_movie.production_companies+=i.companyID+'&'+i['name']+'$'
                    counter+=1
                    if counter==3:
                        break
                new_movie.production_companies=new_movie.production_companies[0:len(new_movie.production_companies)-1]
            
            #Year string
            new_movie.year=movie.get('year')
            #Running time string list
            new_movie.runtimes=movie.get('runtimes')[0]
            
            #Rating 
            imdb_access.update(movie, info=('vote details'))
            new_movie.number_of_votes=movie.get('number of votes')
            
            
            movies.put(new_movie)
            movie_IDs.task_done()
        except Exception ,e:
            print ' - GET_INFO -  An {} exception occured'.format(e),m_id

           # sleep(2)

def store_movies():
    conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
    cur = conn.cursor()
    while True:
        try:
            new_movie = movies.get()
            cur.execute(
                "INSERT INTO new_movies values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (new_movie.id, 
                        new_movie.title,
                        new_movie.cover_url,
                        new_movie.genres,
                        new_movie.color_info,
                        new_movie.director,
                        new_movie.cast_1,
                        new_movie.cast_2,
                        new_movie.cast_3,
                        new_movie.countries,
                        new_movie.languages,
                        new_movie.writer,
                        new_movie.editor,
                        new_movie.cinematographer,
                        new_movie.art_director,
                        new_movie.costume_designer,
                        new_movie.composer,
                        new_movie.sound_mix,
                        new_movie.production_companies,
                        new_movie.year,
                        new_movie.runtimes,
                        new_movie.number_of_votes[1],
                        new_movie.number_of_votes[2],
                        new_movie.number_of_votes[3],
                        new_movie.number_of_votes[4],
                        new_movie.number_of_votes[5],
                        new_movie.number_of_votes[6],
                        new_movie.number_of_votes[7],
                        new_movie.number_of_votes[8],
                        new_movie.number_of_votes[9],
                        new_movie.number_of_votes[10],
                ))
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
