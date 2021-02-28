from test.app_base_test_case import AppBaseTestCase

class AppTest(AppBaseTestCase):
    def test_ping(self):
        result = self.app.get(
            '/ping'
        )
        self.assertEqual(result.data.decode('utf-8'), 'pong')