import sqlite3


def create_table():
    # connect to database
    DB = sqlite3.connect('movie.db')
    # cursor of database
    cDB = DB.cursor()

    # delete all table in database
    cDB.execute("DROP TABLE feature")
    print "-INIT- Table feature has been deleted."
    cDB.execute("DROP TABLE rating")
    print "-INIT- Table rating has been deleted."

    # create info table
    cDB.execute("CREATE TABLE feature (\n"
    + "id TEXT PRIMARY KEY NOT NULL,\n"
    + "title TEXT NOT NULL,\n"
    + "cover_url TEXT NOT NULL,\n"
    + "giant_cover_url TEXT NOT NULL,\n"
    + "genres TEXT NOT NULL,\n"
    + "color_info TEXT DEFAULT NULL,\n"
    + "director TEXT NOT NULL,\n"
    + "cast_1st TEXT NOT NULL,\n"
    + "cast_2nd TEXT DEFAULT NULL,\n"
    + "cast_3rd TEXT DEFAULT NULL,\n"
    + "countries TEXT NOT NULL,\n"
    + "languages TEXT NOT NULL,\n"
    + "writor TEXT DEFAULT NULL,\n"
    + "editor TEXT DEFAULT NULL,\n"
    + "cinematographer TEXT DEFAULT NULL,\n"
    + "art_director TEXT DEFAULT NULL,\n"
    + "costume_designer TEXT DEFAULT NULL,\n"
    + "original_music TEXT DEFAULT NULL,\n"
    + "sound_mix TEXT DEFAULT NULL,\n"
    + "production_companies TEXT NOT NULL,\n"
    + "year INTEGER NOT NULL,\n"
    + "runtimes INTEGER NOT NULL"
    # + "budget INTEGER NOT NULL"
    + ")")
    print "-INIT- Table feature has been created."

    cDB.execute("CREATE TABLE rating("
    + "id TEXT PRIMARY KEY NOT NULL,\n"
    + "type TEXT  NOT NULL,\n"
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
    + "predict_1 REAL DEFAULT NULL,\n"
    + "predict_2 REAL DEFAULT NULL,\n"
    + "predict_3 REAL DEFAULT NULL,\n"
    + "predict_4 REAL DEFAULT NULL,\n"
    + "predict_5 REAL DEFAULT NULL,\n"
    + "predict_6 REAL DEFAULT NULL,\n"
    + "predict_7 REAL DEFAULT NULL,\n"
    + "predict_8 REAL DEFAULT NULL,\n"
    + "predict_9 REAL DEFAULT NULL,\n"
    + "predict_10 REAL DEFAULT NULL"
    + ")")
    print "-INIT- Table rating has been created."

    # save change
    DB.commit()
    # disconnect to database
    DB.close()
    print "-INIT- Database initalization is successful."


if __name__ == '__main__':
    create_table()