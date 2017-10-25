import sqlite3
from movie import Movie
from imdb import imdb,IMDbError,IMDbDataAccessError
import imdb.parser.http.movieParser


## Below are constants associated with IMDB data

imdb_new_movie_url='http://www.imdb.com/movies-coming-soon/'

imdb_access = imdb.IMDb()



def get_Info():
        try:

            # m_id = '4649466'

            # movie = imdb_access.get_movie(m_id)
            # # for i in movie:
            # imdb_access.update(movie, info=('business'))
            # print movie.get('Budget')

            mvIN = imdb_access.get_movie('3460252')
            # create new Movie object
            mvOJ = Movie()

            # title string

            # running time int
            if mvIN.has_key('runtimes'):
                print mvIN.get('runtimes')
                if str(mvIN.get('runtimes')[0]).find(':') != -1:
                    mvOJ.runtimes = str(mvIN.get('runtimes')[0]).split(':')[1]
                    print int(mvOJ.runtimes)
                else:
                    mvOJ.runtimes = mvIN.get('runtimes')[0]
                    print mvOJ.runtimes
            else:
                mvOJ.runtimes = 0


            

 
        except imdb.IMDbError , e:

            #movieID.put(m_id)

            print ' - GET_INFO - An {} exception occured'.format(e)



if __name__ == '__main__':

   # thread_Init()

#    get_ID()

   # movieID.join()
    # db()
    get_Info()

    print 'Done crawling data from IMDB!'