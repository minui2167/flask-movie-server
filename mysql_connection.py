import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = 'yh-db.chyowr2bx2g2.ap-northeast-2.rds.amazonaws.com',
        database = 'movie_review_server',
        user = 'movie_user',
        password = 'movie1234'
    )
    return connection