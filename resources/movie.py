import datetime
from http import HTTPStatus
from os import access
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MovieListResource(Resource):

    def get(self):

        # 1. 클라이언트로부터 데이터 받아온다.
        offset = request.args['offset']
        limit = request.args['limit']
        order = request.args['order']

        try :
            connection = get_connection()

            query = '''select m.title, count(m.id) as cnt, AVG(rating) as avg
                    from movie as m
                    left join rating as r
                    on m.id = r.movie_id
                    group by m.id
                    order by '''+order+''' desc
                    limit '''+offset+''' , '''+limit+''';'''

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # Decimal to String
            i = 0
            for record in result_list :
                result_list[i]['avg'] = float(record['avg'])
                i = i + 1            

            print(result_list)

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error": str(e)}, 503


        return { "result" : "success" , 
                "count" : len(result_list),
                "result_list" : result_list}, 200

class MovieResource(Resource):
     
    def get(self, movie_id):

        try :
            connection = get_connection()

            query = '''select m.*, AVG(rating) as avg, count(m.id) as cnt
                    from movie as m
                    left join rating as r
                    on m.id = r.movie_id
                    group by m.id having m.id = %s;'''

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)
            record = (movie_id, )

            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # Decimal to String
            i = 0
            for record in result_list :
                result_list[i]['year'] = record['year'].isoformat()
                result_list[i]['createdAt'] = record['createdAt'].isoformat()
                result_list[i]['avg'] = str(record['avg'])
                i = i + 1            

            print(result_list)

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error": str(e)}, 503


        return { "result" : "success" , 
                "count" : len(result_list),
                "result_list" : result_list}, 200