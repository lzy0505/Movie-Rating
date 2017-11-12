from flask import Flask,render_template,request,url_for,redirect
from flask_nav import Nav,register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_frozen import Freezer
import database


lFtrCols = ["title","year", "runtimes","genres", 'color_info', 'director', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
               'editor', 'cinematographer', 'art_director', 'costume_designer',
               'original_music', 'sound_mix', 'production_companies']

info_name={'title':'Title','genres':'Genres','color_info':'Color','director':'Director','cast_1st':'1st Actor(Actress)','cast_2nd':'2nd Actor(Actress)','cast_3rd':'3rd Actor(Actress)','countries':'Country','languages':'Language',
'writer':'Writer','editor':'Editor','cinematographer':'Cinematographer','art_director':'Art Direction','costume_designer':'Costume Designer','original_music':'Original music by','sound_mix':'Sound Mix',
'production_companies':'Production Company','cheby':'Chebyshev','clark':'Clark','cbra':'Canberra','k-l':'Kullback-Leibler','cos':'Cosine','intsc':'Intersection'}

indices=['cheby','clark','cbra','k-l','cos','intsc']


class CustomRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(CustomRenderer, self).visit_Navbar(node)
        nav_tag['class'] += ' navbar-fixed-top'
        return nav_tag

nav=Nav()

nav.register_element('top', Navbar(
    # Link('Tech Support', href='http://techsupport.invalid/widgits_inc')
    # ,
    "Movie Rating Project",
    View('Index', 'preview')
))

app = Flask(__name__)
app.config['FREEZER_RELATIVE_URLS'] = True
register_renderer(app, 'custom', CustomRenderer)

nav.init_app(app)

Bootstrap(app)

freezer = Freezer(app)


@freezer.register_generator
def details():
    for m in database.select_movie():
        yield {'movieid': m[0].encode('utf-8')}

# @app.route('/')
# def home():
#     movies=database.select_movie()
#     return render_template('index_layout.html',movies=movies)
    # return redirect(url_for('preview'))

@app.route('/preview/')
def preview():
    movies=database.select_movie()
    return render_template('index_layout.html',movies=movies)

@app.route('/details/<movieid>/')
def details(movieid):
    movie=database.get_instance_details(movieid)
    return render_template('details_layout.html',info_cols=lFtrCols,movie=movie,name=info_name,metrics=indices)


if __name__ == '__main__':
    # freezer.freeze()
    freezer.run(debug=True)
   	# app.run()