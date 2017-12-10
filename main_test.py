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

    def test_Manifest(self):
        # AddManifest Test
        test_file = open('./test.json', 'r')
        post_contents = {'file_data': test_file.read()}
        request = webapp2.Request.blank('/api/manifest/add', POST=post_contents)
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'Upload Manifest success!')

        # SearchManifest Test
        request = webapp2.Request.blank('/0xffff')
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)


    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
