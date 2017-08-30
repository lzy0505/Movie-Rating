from flask import Flask,render_template,request,url_for,redirect
import MySQLdb
import database


info_cols=['title','year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']



app = Flask(__name__)



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
    return render_template('new_details_layout.html',info_cols=info_cols,movie=movie)

@app.route('/olddetails/<movieid>')
def olddetails(movieid):
    movie=database.get_instance_details('new_movies',movieid)
    return render_template('old_details_layout.html',info_cols=info_cols,movie=movie)


if __name__ == '__main__':
    app.run()