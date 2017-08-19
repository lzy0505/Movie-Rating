from flask import Flask,render_template,request,url_for
import MySQLdb
import database

app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index_layout.html')

@app.route('/oldtable')
def oldtable():
    movies=database.get_instance_basic("new_movies")
    return render_template('old_index_layout.html',movies=movies)


@app.route('/newtable')
def newtable():
    movies=database.get_instance_basic("future_movies")
    return render_template('new_index_layout.html',movies=movies)

if __name__ == '__main__':
    app.run()