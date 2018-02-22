from flask import Flask,render_template,request,url_for,redirect
import database

# lFtrCols = ["title","year", "runtimes","genres", 'color_info', 'director', 'cast_1st',
#                'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
#                'editor', 'cinematographer', 'art_director', 'costume_designer',
#                'original_music', 'sound_mix', 'production_companies']

# info_name={'title':'Title','genres':'Genres','color_info':'Color','director':'Director','cast_1st':'1st Actor(Actress)','cast_2nd':'2nd Actor(Actress)','cast_3rd':'3rd Actor(Actress)','countries':'Country','languages':'Language',
# 'writer':'Writer','editor':'Editor','cinematographer':'Cinematographer','art_director':'Art Direction','costume_designer':'Costume Designer','original_music':'Original music by','sound_mix':'Sound Mix',
# 'production_companies':'Production Company','cheby':'Chebyshev','clark':'Clark','cbra':'Canberra','k-l':'Kullback-Leibler','cos':'Cosine','intsc':'Intersection'}

# indices=['cheby','clark','cbra','k-l','cos','intsc']


application = Flask(__name__)



@application.route('/')
def home():
    etrs=database.perfect_prediction()
    return render_template('index.html',entries=etrs)

@application.route('/about/')
def about():
    return render_template('about.html')

@application.route('/list/')
def mlist():
    etrs=database.select_movie()
    return render_template('ratinglist.html',entries=etrs)

@application.route('/<movieid>/')
def entries(movieid):
    etry=database.get_instance_details(movieid)
    return render_template('single.html',entry=etry)

# @app.route('/details/<movieid>/')
# def details(movieid):
#     movie=database.get_instance_details(movieid)
#     return render_template('details_layout.html',info_cols=lFtrCols,movie=movie,name=info_name,metrics=indices)


if __name__ == '__main__':
   	application.run()