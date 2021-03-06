import pymysql


def create_table():
    # connect to database
    connection = pymysql.connect(host='movie-data.ch6y02vfazod.ap-northeast-1.rds.amazonaws.com',
                            user='admin',
                            password='123',
                            database='movierating',
                            port=3306,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    # cursor of database
    with connection.cursor() as cursor:

        # delete all table in database
        cursor.execute("DROP TABLE `data`")
        print ("-INIT- Table data has been deleted.")
        # cursor.execute("DROP TABLE `rating`")
        # print ("-INIT- Table rating has been deleted.")

        # create info table
        cursor.execute("CREATE TABLE `data` ("
        + "`for` TEXT NOT NULL,"
        + "`id` VARCHAR(7) NOT NULL,"
        + "`title` TEXT NOT NULL,"
        + "`cover_url` TEXT NOT NULL,"
        + "`giant_cover_url` TEXT NOT NULL,"
        + "`genres` TEXT NOT NULL,"
        + "`color_info` TEXT DEFAULT NULL,"
        + "`cast_1st` TEXT NOT NULL,"
        + "`cast_2nd` TEXT DEFAULT NULL,"
        + "`cast_3rd` TEXT DEFAULT NULL,"
        + "`countries` TEXT NOT NULL,"
        + "`languages` TEXT NOT NULL,"
        + "`director` TEXT NOT NULL,"
        + "`writer` TEXT DEFAULT NULL,"
        + "`producer` TEXT DEFAULT NULL,"
        + "`composers` TEXT DEFAULT NULL,"
        + "`cinematographer` TEXT DEFAULT NULL,"
        + "`editor` TEXT DEFAULT NULL,"
        + "`art_director` TEXT DEFAULT NULL,"
        + "`costume_designer` TEXT DEFAULT NULL,"
        + "`production_companies` TEXT NOT NULL,"
        + "`year` SMALLINT NOT NULL,"
        + "`month` SMALLINT NOT NULL,"
        + "`runtimes` SMALLINT NOT NULL,"
        + "`metric` REAL DEFAULT NULL,"
        + "`real_1` REAL DEFAULT NULL,"
        + "`real_2` REAL DEFAULT NULL,"
        + "`real_3` REAL DEFAULT NULL,"
        + "`real_4` REAL DEFAULT NULL,"
        + "`real_5` REAL DEFAULT NULL,"
        + "`real_6` REAL DEFAULT NULL,"
        + "`real_7` REAL DEFAULT NULL,"
        + "`real_8` REAL DEFAULT NULL,"
        + "`real_9` REAL DEFAULT NULL,"
        + "`real_10` REAL DEFAULT NULL,"
        + "`predict_1` REAL DEFAULT NULL,"
        + "`predict_2` REAL DEFAULT NULL,"
        + "`predict_3` REAL DEFAULT NULL,"
        + "`predict_4` REAL DEFAULT NULL,"
        + "`predict_5` REAL DEFAULT NULL,"
        + "`predict_6` REAL DEFAULT NULL,"
        + "`predict_7` REAL DEFAULT NULL,"
        + "`predict_8` REAL DEFAULT NULL,"
        + "`predict_9` REAL DEFAULT NULL,"
        + "`predict_10` REAL DEFAULT NULL,"
        + "`stamp_text` TEXT DEFAULT NULL,"
        + "`stamp_time` TEXT DEFAULT NULL,"
        + "PRIMARY KEY(`id`)"
        + ");")
        print ("-INIT- Table data has been created.")

    # save change
    connection.commit()
    # disconnect to database
    connection.close()
    print ("-INIT- Database initalization is successful.")


if __name__ == '__main__':
    create_table()