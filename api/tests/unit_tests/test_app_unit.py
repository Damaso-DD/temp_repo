from app import app, get_redis
from unittest import mock, TestCase

class TestApp(TestCase):

    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()


    def tearDown(self) -> None:
        self.ctx.pop()

    @mock.patch("app.get_redis")
    def test_get_suggestions(self, get_redis_mock):
        data = ['[["Rice"], ["Yam"]]']
        redis_mock = mock.Mock()
        get_redis_mock.return_value = redis_mock
        redis_mock.llen = mock.Mock(return_value=1)
        redis_mock.lrange = mock.Mock(return_value=data)
        response = self.client.get('/food')
        assert response.json['suggestions'] == [{'name': 'Rice'}, {'name': 'Yam'}]
        self.assertEqual(200, response.status_code)
    
    @mock.patch("app.celery")
    def test_post_suggestions(self, celery_mock):
        food_suggestion = 'Rice'
        celery_mock.send_task = mock.Mock()
        response = self.client.post('/food',
                        json={'food': food_suggestion})
        self.assertEqual(response.status_code, 200)
        celery_mock.send_task.assert_called_once_with('tasks.update_database', (food_suggestion,))
            
    @mock.patch("app.Redis")
    def test_get_redis(self, redis_mock):
        redis_mock_out = mock.Mock()
        redis_mock.return_value = redis_mock_out
        obj = get_redis()
        self.assertEqual(obj, redis_mock_out)