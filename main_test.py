import sys
import unittest
sys.path.append('/home/travis/google-cloud-sdk/platform/google_appengine')
from google.appengine.ext import testbed
from google.appengine.ext import ndb
import webapp2
import main


class TestHandlers(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def test_AddManifestAndPort(self):
        # AddManifest
        post_contents1 = {'name': 'LED', 'description': 'LED light', 'author': 'MakTak'}
        request = webapp2.Request.blank('/api/manifest/addmanifest', POST=post_contents1)
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)

        # AddPort
        post_contents2 = {'port_number': '1', 'name': 'red', 'description': 'red LED',
                         'permission': 'RW', 'type': 'int16'}
        request = webapp2.Request.blank('/api/manifest/addport/65535', POST=post_contents2)
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
