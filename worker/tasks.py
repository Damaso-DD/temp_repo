import psycopg2
import json
import os

from celery import Celery
from celery.schedules import crontab
from redis import Redis

BROKER_URL = 'redis://redis:6379/0'

celeryapp = Celery('main', broker=BROKER_URL)

def get_redis():
    redis_conn = Redis(host="redis", db=0, socket_timeout=5)
    return redis_conn


@celeryapp.task
def update_database(food_suggestion):
    session = connect_to_db()
    cursor = session.cursor()
    insert_query = f"""
                    INSERT INTO food_suggestions (food, created_at) 
                    VALUES ('{food_suggestion}', NOW())
                    """
    cursor.execute(insert_query)
    session.commit()
    cursor.close()
    session.close()

@celeryapp.task(name='tasks.fetch_suggestions')
def fetch_suggestions():
    session = connect_to_db()
    cursor = session.cursor()
    select_query = """
                    select food from food_suggestions;
                    """
    cursor.execute(select_query)
    suggestions = cursor.fetchall()
    redis_conn = get_redis()
    if redis_conn.exists('suggestions'):
        redis_conn.delete('suggestions')
    redis_conn.rpush("suggestions", json.dumps(suggestions))
    session.commit()
    cursor.close()
    session.close()

def connect_to_db():
    db = psycopg2.connect(
        host="postgres",
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD")
    )
    return db


celeryapp.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'tasks.fetch_suggestions',
        'schedule': 5,
    },
}