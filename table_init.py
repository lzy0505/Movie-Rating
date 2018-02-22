import sqlite3


def create_table():
    # connect to database
    DB = sqlite3.connect('movie.db')
    # cursor of database
    cDB = DB.cursor()

    # delete all table in database
    cDB.execute("DROP TABLE feature")
    print ("-INIT- Table feature has been deleted.")
    cDB.execute("DROP TABLE rating")
    print ("-INIT- Table rating has been deleted.")

    # create info table
    cDB.execute("CREATE TABLE feature (\n"
    + "for TEXT  NOT NULL,\n"
    + "id TEXT PRIMARY KEY NOT NULL,\n"
    + "title TEXT NOT NULL,\n"
    + "cover_url TEXT NOT NULL,\n"
    + "giant_cover_url TEXT NOT NULL,\n"
    + "genres TEXT NOT NULL,\n"
    + "color_info TEXT DEFAULT NULL,\n"
    + "cast_1st TEXT NOT NULL,\n"
    + "cast_1st_rank INTEGER NOT NULL,\n"
    + "cast_2nd TEXT DEFAULT NULL,\n"
    + "cast_2nd_rank INTEGER DEFAULT NULL,\n"
    + "cast_3rd TEXT DEFAULT NULL,\n"
    + "cast_3rd_rank INTEGER DEFAULT NULL,\n"
    + "countries TEXT NOT NULL,\n"
    + "languages TEXT NOT NULL,\n"
    + "director TEXT NOT NULL,\n"
    + "writer TEXT DEFAULT NULL,\n"
    + "producer TEXT DEFAULT NULL,\n"
    + "composers TEXT DEFAULT NULL,\n"
    + "cinematographer TEXT DEFAULT NULL,\n"
    + "editor TEXT DEFAULT NULL,\n"
    + "art_director TEXT DEFAULT NULL,\n"
    + "costume_designer TEXT DEFAULT NULL,\n"
    + "production_companies TEXT NOT NULL,\n"
    + "year INTEGER NOT NULL,\n"
    + "runtimes INTEGER NOT NULL"
    + ")")
    print ("-INIT- Table feature has been created.")

    cDB.execute("CREATE TABLE rating("
    + "id TEXT PRIMARY KEY NOT NULL,\n"
    + "metric REAL DEFAULT NULL,\n"
    + "real_1 REAL DEFAULT NULL,\n"
    + "real_2 REAL DEFAULT NULL,\n"
    + "real_3 REAL DEFAULT NULL,\n"
    + "real_4 REAL DEFAULT NULL,\n"
    + "real_5 REAL DEFAULT NULL,\n"
    + "real_6 REAL DEFAULT NULL,\n"
    + "real_7 REAL DEFAULT NULL,\n"
    + "real_8 REAL DEFAULT NULL,\n"
    + "real_9 REAL DEFAULT NULL,\n"
    + "real_10 REAL DEFAULT NULL,\n"
    + "o_predict_1 REAL DEFAULT NULL,\n"
    + "o_predict_2 REAL DEFAULT NULL,\n"
    + "o_predict_3 REAL DEFAULT NULL,\n"
    + "o_predict_4 REAL DEFAULT NULL,\n"
    + "o_predict_5 REAL DEFAULT NULL,\n"
    + "o_predict_6 REAL DEFAULT NULL,\n"
    + "o_predict_7 REAL DEFAULT NULL,\n"
    + "o_predict_8 REAL DEFAULT NULL,\n"
    + "o_predict_9 REAL DEFAULT NULL,\n"
    + "o_predict_10 REAL DEFAULT NULL,\n"
    + "p_predict_1 REAL DEFAULT NULL,\n"
    + "p_predict_2 REAL DEFAULT NULL,\n"
    + "p_predict_3 REAL DEFAULT NULL,\n"
    + "p_predict_4 REAL DEFAULT NULL,\n"
    + "p_predict_5 REAL DEFAULT NULL,\n"
    + "p_predict_6 REAL DEFAULT NULL,\n"
    + "p_predict_7 REAL DEFAULT NULL,\n"
    + "p_predict_8 REAL DEFAULT NULL,\n"
    + "p_predict_9 REAL DEFAULT NULL,\n"
    + "p_predict_10 REAL DEFAULT NULL"
    + ")")
    print ("-INIT- Table rating has been created.")

    # save change
    DB.commit()
    # disconnect to database
    DB.close()
    print ("-INIT- Database initalization is successful.")


if __name__ == '__main__':
    create_table()