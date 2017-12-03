# -*- coding:utf-8 -*-
from flask import Flask,render_template,redirect
from flask_nav import Nav,register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
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

application = Flask(__name__)

register_renderer(application, 'custom', CustomRenderer)

nav.init_app(application)

Bootstrap(application)



@application.route('/')
def home():
    return redirect(url_for('preview'))

@application.route('/preview/')
def preview():
    movies=database.select_movie()
    return render_template('index_layout.html', movies=movies)

@application.route('/details/<movieid>/')
def details(movieid):
    movie=database.get_instance_details(movieid)
    return render_template('details_layout.html',info_cols=lFtrCols,movie=movie,name=info_name,metrics=indices)


if __name__ == '__main__':
   	application.run()