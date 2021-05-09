import requests
from pprint import pprint
import unittest

interactive = False

# Change var above to do manual runs
# I'm lazy and I didn't make this a sys argv


def run_interactive_test():
    email = input("What's the customer email? ")
    name = input("And their name? ")
    url = 'http://127.0.0.1:5000/post_data?email=' + email + '&name=' + name

    resp = requests.post(url)
    resp.raise_for_status()
    pprint(resp.json())


class TestEmailServer(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:5000'

    def test_base_url_teapot(self):
        resp = requests.get(
            self.base_url)
        self.assertEqual(resp.status_code, 418)

    def test_get_data_invalid(self):
        resp = requests.get(
            self.base_url + '/get_data')
        self.assertEqual(resp.status_code, 400)

    def test_get_data_nonexistent(self):
        resp = requests.get(
            self.base_url + '/get_data?email=doesnotexist@example.org')
        self.assertIsNotNone(resp.content)
        self.assertEqual(resp.status_code, 404)

    def test_get_data_valid(self):
        resp = requests.get(
            self.base_url + '/get_data?email=foobar@example.org')
        self.assertEqual(resp.content, 'cassie'.encode('UTF-8'))
        self.assertEqual(resp.status_code, 200)

    def test_post_data_invalid(self):
        resp = requests.post(
            self.base_url + '/post_data')
        self.assertEqual(resp.status_code, 400)

    def test_post_data_nonexistent(self):
        resp = requests.post(
            self.base_url + '/post_data?email=doesnotexist@example.org&name=barbaz')
        self.assertIsNotNone(resp.content)
        self.assertEqual(resp.status_code, 404)

    def test_post_data_valid(self):
        resp = requests.post(
            self.base_url + '/post_data?email=foobar@example.org&name=barbaz')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(type(resp.json() is dict))

        # Reset back to default; probably shouldn't hardcode...
        resp = requests.post(
            self.base_url + '/post_data?email=foobar@example.org&name=cassie')


if __name__ == "__main__":
    if interactive:
        run_interactive_test()
    else:
        unittest.main()
