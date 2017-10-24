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

            mvIN = imdb_access.get_movie('4649466')
            # create new Movie object
            mvOJ = Movie()
            # ID string
            mvOJ.id = '4649466'
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
            print type(mvOJ.cast_1st)
            if len(mvIN.get('cast')) >= 2:
                # 2nd Actor
                mvOJ.cast_2nd = mvIN.get('cast')[1]['name']
            if len(mvIN.get('cast')) >= 3:
                # 3rd Actor
                mvOJ.cast_3rd = mvIN.get('cast')[2]['name']
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
            # running time int
            if mvIN.has_key('runtimes'):
                if str(mvIN.get('runtimes')[0]).find(':') != -1:
                    mvOJ.runtimes = str(mvIN.get('runtimes')[0]).split(':')[1]
                else:
                    mvOJ.runtimes = mvIN.get('runtimes')[0]
            imdb_access.update(mvIN, info=('vote details'))
            mvOJ.number_of_votes = mvIN.get('number of votes')

            ssum = 0.0
            rating = []
            type(mvOJ.number_of_votes)
            for n in mvOJ.number_of_votes:
                ssum+=mvOJ.number_of_votes[n]
                rating.append(mvOJ.number_of_votes[n])
            for i in xrange(0,len(rating)):
                rating[i]=rating[i]/ssum
            print rating

            # for i in [mvOJ.id,
            #         mvOJ.title,
            #         mvOJ.cover_url,
            #         mvOJ.giant_cover_url,
            #         mvOJ.genres,
            #         mvOJ.color_info,
            #         mvOJ.director,
            #         mvOJ.cast_1st,
            #         mvOJ.cast_2nd,
            #         mvOJ.cast_3rd,
            #         mvOJ.countries,
            #         mvOJ.languages,
            #         mvOJ.writer,
            #         mvOJ.editor,
            #         mvOJ.cinematographer,
            #         mvOJ.art_director,
            #         mvOJ.costume_designer,
            #         mvOJ.original_music,
            #         mvOJ.sound_mix,
            #         mvOJ.production_companies,
            #         mvOJ.year,
            #         mvOJ.runtimes]:
            #     print i


            # conn = sqlite3.connect("movie.db")
            # cur = conn.cursor()
            # cur.execute(
            #     "INSERT INTO feature values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            #     (mvOJ.id,
            #         mvOJ.title,
            #         mvOJ.cover_url,
            #         mvOJ.giant_cover_url,
            #         mvOJ.genres,
            #         mvOJ.color_info,
            #         mvOJ.director,
            #         mvOJ.cast_1st,
            #         mvOJ.cast_2nd,
            #         mvOJ.cast_3rd,
            #         mvOJ.countries,
            #         mvOJ.languages,
            #         mvOJ.writer,
            #         mvOJ.editor,
            #         mvOJ.cinematographer,
            #         mvOJ.art_director,
            #         mvOJ.costume_designer,
            #         mvOJ.original_music,
            #         mvOJ.sound_mix,
            #         mvOJ.production_companies,
            #         mvOJ.year,
            #         mvOJ.runtimes))
            
        except imdb.IMDbError , e:

            #movieID.put(m_id)

            print ' - GET_INFO - An {} exception occured'.format(e)


def db():
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO feature values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ("1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "8",
    "7",
    "9",
    "0",
    "1",
    "2"
    ))

if __name__ == '__main__':

   # thread_Init()

#    get_ID()

   # movieID.join()
    # db()
    get_Info()

    print 'Done crawling data from IMDB!'