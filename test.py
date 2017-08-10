import requests



from imdb import imdb,IMDbError,IMDbDataAccessError

from bs4 import BeautifulSoup

from Queue import Queue

from threading import Thread

#from defination import Movie



thread_number = 5



## Below are constants associated with IMDB data

imdb_new_movie_url='http://www.imdb.com/movies-coming-soon/'

imdb_access = imdb.IMDb()

imdb_access.reraiseException=True



# the multi-processor queue of movie IDs

movieID = Queue(maxsize = 500)



# the time range where we search for movies

begin_year = 2017

end_year = 2017



begin_month = 7

end_month = 7







def get_ID():

    for year, month in zip(range(begin_year, end_year+1), range(begin_month, end_month+1)):

        url = imdb_new_movie_url + ( '%d-%02d' % (year, month) )



        print " - GET_ID - movie url: ", url



        soup = BeautifulSoup(requests.get(url).content, "lxml")



        list_item = soup.findAll(True, {'class': "list_item"})

        for item in list_item:

            h4 = item.findAll('h4')

            for h in h4:

                link = h.find('a').get('href')

                link = link[9: link.index('?')-1]

                movieID.put(link)

                print " - GET_ID - link: ", link



def get_Info():

   # while True:

        try:

            m_id = '5013056'

            # #movieID.get()

            movie = imdb_access.get_movie(m_id)


            # #ID string

            # print  m_id

            # #Title string

            # print  movie.get('title')

            # #Poster url string

            # print  movie.get('cover url')



            # #Genres string list

            # print movie.get('genres')


            # #Color string list

            # print movie.get('color info')

            # #Director string list

            # print movie.get('director')
           
            # #1st Actor

            # print movie.get('cast')[0]

            # #2nd Actor

            # print movie.get('cast')[1]

            # #3rd Actor

            # print movie.get('cast')[2]

            # #Country string list

            # print  movie.get('countries')

            # #Language string list

            # print  movie.get('languages')

            # #Writer string list

            # print  movie.get('writer')

            # #Editor string list

            # print  movie.get('editor')

            # #Cinematographer string list

            # print  movie.get('cinematographer')

            # #Art direction string list

            # print  movie.get('art direction')

            # #Costume designer string list

            # print  movie.get('costume designer')

            # #Music By string list

            # print  movie.get('original music')

            # #Sound string list

            # print  movie.get('sound mix')

            #Production company string list

            # print  movie.get('production companies')
           
            # temp=''
            # counter=0
            # temp=movie.get('production companies')
            # for i in movie.get('production companies'):
            #     print i.companyID
                #temp+=i.getID()+'&'+i['name']+'$'
                #counter+=1
                #if counter==3:
                #    break
            #print temp[0:len(temp)-1]
            
            

            # #Year string

            # print  movie.get('year')

            # #Running time string list

            # print  movie.get('runtimes')

            print movie.get('runtimes')

            # #Rating 

            # imdb_access.update(movie, info=('vote details'))

            # print  movie.get('number of votes')
            
          # movieID.task_done()

        except imdb.IMDbDataAccessError , e:

            #movieID.put(m_id)

            print ' - GET_INFO - An {} exception occured'.format(e)





def thread_Init():

    for i in range(thread_number):

        t=Thread(target=get_Info)

        t.deamon = True

        t.start()





if __name__ == '__main__':

   # thread_Init()

   # get_ID()

   # movieID.join()

    get_Info()

    print 'Done crawling data from IMDB!'