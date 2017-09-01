from flask import Flask,render_template,request,url_for,redirect
import MySQLdb
from flask_nav import Nav,register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
import database


info_cols=['title','year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']

info_name={'title':'Title','genres':'Genres','color_info':'Color','director':'Director','cast_1':'1st Actor(Actress)','cast_2':'2nd Actor(Actress)','cast_3':'3rd Actor(Actress)','countries':'Country','languages':'Language',
'writer':'Writer','editor':'Editor','cinematographer':'Cinematographer','art_direction':'Art Direction','costume_designer':'Costume Designer','original_music':'Original music by','sound_mix':'Sound Mix',
'production_companies':'Production Company'}


class CustomRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(CustomRenderer, self).visit_Navbar(node)
        nav_tag['class'] += ' navbar-fixed-top'
        return nav_tag

nav=Nav()

nav.register_element('top', Navbar(
    "Movie Rating Project",
    View('Old Movies Rating Comparing', 'oldpreview'),
    View('New Movies Rating Predicting', 'newpreview')
))

app = Flask(__name__)
register_renderer(app, 'custom', CustomRenderer)

nav.init_app(app)

Bootstrap(app)






@app.route('/')
def home():
    return redirect(url_for('oldpreview'))

@app.route('/oldpreview')
def oldpreview():
    movies=database.get_instance_basic("new_movies")
    return render_template('old_index_layout.html',movies=movies)


@app.route('/newpreview')
def newpreview():
    movies=database.get_instance_basic("future_movies")
    return render_template('new_index_layout.html',movies=movies)

@app.route('/newdetails/<movieid>')
def newdetails(movieid):
    movie=database.get_instance_details('future_movies',movieid)
    return render_template('new_details_layout.html',info_cols=info_cols,movie=movie,name=info_name)

@app.route('/olddetails/<movieid>')
def olddetails(movieid):
    movie=database.get_instance_details('new_movies',movieid)
    return render_template('old_details_layout.html',info_cols=info_cols,movie=movie,name=info_name)


if __name__ == '__main__':
    app.run()