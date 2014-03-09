import json
import sf_bikes
import unittest

class SfBikeTestCase(unittest.TestCase):
    def setUp(self):
        sf_bikes.app.config.update(dict(
            TESTING = True,
            DEBUG = False
        ))
        self.app = sf_bikes.app.test_client()

class SpotsTestCase(SfBikeTestCase):
    def testMissingId(self):
      response = self.app.get('/spots/-1')
      self.assertEqual(response.status_code, 404)

    def testInvalidId(self):
      response = self.app.get('/spots/abc')
      self.assertEqual(response.status_code, 400)

    def testSpotInfo(self):
        response = self.app.get('/spots/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['location'],
            'John Muir and Skyline Blvd (Fort Funston, main lot)'
        )

class SpotsInBoundTestCase(SfBikeTestCase):
    def testMissingArg(self):
        response = self.app.get('/spots/bounds?bounds=1,2,3')
        self.assertEqual(response.status_code, 400)

    def testInvalidArg(self):
        response = self.app.get('/spots/bounds?bounds=1,2,3,abc')
        self.assertEqual(response.status_code, 400)

    def testValidRequest(self):
        response = self.app.get('/spots/bounds?bounds=1,2,3,4')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(type(data['result']), list)

if __name__ == '__main__':
    unittest.main()
