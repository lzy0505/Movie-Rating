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
    database.connect_to_sql()
    perfect_etrs=database.perfect_prediction()
    recent_etrs=database.recent_prediction()
    return render_template('index.html',entries1=perfect_etrs,entries2=recent_etrs)

@application.route('/about/')
def about():
    return render_template('about.html')

@application.route('/list/')
def mlist():
    database.connect_to_sql()
    etrs=database.select_movie()
    return render_template('ratinglist.html',entries=etrs)

@application.route('/<movieid>/')
def entries(movieid):
    database.connect_to_sql()
    etry=database.get_instance_details(movieid)
    return render_template('single.html',entry=etry)

# @app.route('/details/<movieid>/')
# def details(movieid):
#     movie=database.get_instance_details(movieid)
#     return render_template('details_layout.html',info_cols=lFtrCols,movie=movie,name=info_name,metrics=indices)


if __name__ == '__main__':
   	application.run(debug=True)