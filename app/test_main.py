import unittest
from app import app
import time


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_result(self):
        response = self.app.post(f'/result')
        self.assertEqual(response.status_code, 200)

        # We verify that in that obivous case the first given answer is the anime that the used searched
        self.assertEqual(str(response.data).split("<li>")[1].split("</li>")[0], "Cowboy Bebop - Sunrise  Score:<b>8.81</b>")

    def test_stress(self):
        t0 = time.time()
        for i in range(20):
            self.app.post(f'/result')
        t1 = time.time()
        self.assertEqual(t1-t0 < 0.20, True)

        


if __name__ == '__main__':
    unittest.main()
