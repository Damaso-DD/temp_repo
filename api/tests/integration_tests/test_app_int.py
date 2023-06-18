# api/tests/integration_tests/test_app_int.py
import psycopg2

from app import app
from time import sleep
from unittest import TestCase

class TestIntegrations(TestCase):

    def setUp(self) -> None:
        self.db = self.connect_to_db()
        self.cursor = self.db.cursor()

    def connect_to_db(self):
        db = psycopg2.connect(
            host="postgres",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        return db

    def test_suggestions(self):
        # check that the redis cache "suggestions" is initially empty
        response = app.test_client().get('/food')
        self.assertEqual(response.status_code, 200)
        suggestions = response.json['suggestions']
        assert suggestions == []
        # send POST requests to the /food api
        foods = ['Rice', 'Yam', 'Beans']
        for food in foods:
            response = app.test_client().post('/food',
                        json={'food': food})
            
            self.assertEqual(response.status_code, 200)

        # check that the data is now saved in the postgresql database
        sleep(15)

        self.cursor.execute("SELECT food FROM food_suggestions;")
        db_suggestions = self.cursor.fetchall()
        # check that all the foods exist in database
        for food in foods:
            self.assertIn((food,), db_suggestions)
        
        # check that the data is now in the redis cache key "suggestions"
        response = app.test_client().get('/food')
        self.assertEqual(response.status_code, 200)
        redis_suggestions = response.json['suggestions']
        # check that all the foods exist in redis cache
        for food in foods:
            self.assertIn({'name': food}, redis_suggestions)
