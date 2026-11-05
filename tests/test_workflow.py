import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlencode
from wsgiref.util import setup_testing_defaults

from route import create_app


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.sqlite3'
        self.app = create_app(self.path)
        self.cookie = ''

    def tearDown(self):
        self.temp.cleanup()

    def call(self, method, path, data=None, form=False):
        body = (urlencode(data).encode() if form else json.dumps(data).encode()) if data else b''
        env = {}
        setup_testing_defaults(env)
        env.update(REQUEST_METHOD=method, PATH_INFO=path, CONTENT_LENGTH=str(len(body)),
                   CONTENT_TYPE='application/x-www-form-urlencoded' if form else 'application/json',
                   HTTP_COOKIE=self.cookie, **{'wsgi.input': io.BytesIO(body)})
        result = {}
        def start(status, headers, exc_info=None):
            result.update(status=int(status.split()[0]), headers=dict(headers))
        output = b''.join(self.app(env, start)).decode()
        return result, output

    def login(self):
        result, _ = self.call('POST', '/portal', {'username': 'admin', 'password': 'admin123'}, True)
        self.assertEqual(result['status'], 303)
        self.cookie = result['headers']['Set-Cookie'].split(';')[0]

    def test_authentication_and_logout(self):
        self.assertEqual(self.call('GET', '/banco')[0]['status'], 303)
        self.assertEqual(self.call('POST', '/banco', {'titulo': 'X', 'autor': 'Y'})[0]['status'], 401)
        self.assertEqual(self.call('POST', '/portal', {'username': 'admin', 'password': 'errada'}, True)[0]['status'], 401)
        self.login()
        self.assertEqual(self.call('GET', '/banco')[0]['status'], 200)
        self.assertEqual(self.call('POST', '/logout')[0]['status'], 303)
        self.assertEqual(self.call('GET', '/banco')[0]['status'], 303)

    def test_crud_validation_and_persistence(self):
        self.login()
        self.assertEqual(self.call('POST', '/banco', {'titulo': ' ', 'autor': 'X'})[0]['status'], 400)
        result, body = self.call('POST', '/banco', {'titulo': '<script>Oi</script>', 'autor': 'José'})
        self.assertEqual(result['status'], 201)
        book_id = json.loads(body)['id']
        html = self.call('GET', '/banco')[1]
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>Oi</script>', html)
        self.app = create_app(self.path)
        self.cookie = ''
        self.login()
        self.assertIn('José', self.call('GET', '/banco')[1])
        self.assertEqual(self.call('PUT', f'/banco/{book_id}', {'titulo': 'Dom Casmurro', 'autor': 'Machado de Assis'})[0]['status'], 200)
        self.assertIn('Dom Casmurro', self.call('GET', '/banco')[1])
        self.assertEqual(self.call('DELETE', f'/banco/{book_id}')[0]['status'], 204)
        self.assertNotIn('Dom Casmurro', self.call('GET', '/banco')[1])
        self.assertEqual(self.call('DELETE', f'/banco/{book_id}')[0]['status'], 404)
        self.assertEqual(self.call('PUT', f'/banco/{book_id}', {'titulo': 'A', 'autor': 'B'})[0]['status'], 404)


if __name__ == '__main__':
    unittest.main()
