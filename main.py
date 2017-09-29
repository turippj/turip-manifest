#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import cgi
import urllib
import json
import webapp2
import jinja2
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# [ Start DataTemplate ]
class DataTemplate(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
# [ End DataTemplate ]


# [ Start Manifest ]
class Manifest(DataTemplate):
    model = ndb.IntegerProperty()
    author = ndb.StringProperty()

    @classmethod
    def query_manifest(cls):
        return cls.query().order(cls.model)

    # [ port methods ]
    def add(self, content):
        port = Port(parent=self.key,
                    number=content['number'],
                    name=content['name'],
                    description=content['description'],
                    permission=content['permission'],
                    type=content['type'])
        port.put()

    def delete(self, port):
        port.key.delete()

# [ End Manifest ]


# [ Start Port ]
class Port(DataTemplate):
    number = ndb.IntegerProperty()
    permission = ndb.StringProperty()
    type = ndb.StringProperty()
# [ End Port ]


# [ Start JsonFile ]
class JsonFile(ndb.Model):
    file_data = ndb.BlobProperty()
# [ End JsonFile ]


# [ Start AddManifest ]
class AddManifest(webapp2.RequestHandler):
    def get(self, json_id):
        json_file = JsonFile.get_by_id(long(json_id))
        file = json.loads(json_file.file_data)

        model_number = 65535  # The first free model_number
        existing_manifest = Manifest.query(Manifest.model == model_number).get()
        while existing_manifest is not None:
            model_number += 1
            existing_manifest = Manifest.query(Manifest.model == model_number).get()

        manifest = Manifest(
                    model=model_number,
                    name=file['name'],
                    description=file['description'],
                    author=file['author'])
        manifest.put()

        for port in file['port']:
            manifest.add(port)

        json_file.key.delete()

        self.response.write('Upload Manifest success!')


# [ End AddManifest ]


# [ Start UploadJson ]
class UploadJson(webapp2.RequestHandler):
    def post(self):
        file_data = str(self.request.get('file_data'))
        manifest_file = JsonFile()
        manifest_file.file_data = file_data
        manifest_file.put()
        self.redirect('/api/manifest/addmanifest/' + str(manifest_file.key.id()))
# [ End UploadJson ]


# [ Start AddManifestPage ]
class UploadManifestPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('manifest.html')
        self.response.write(template.render())
# [ End AddManifestPage ]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/manifest/uploadjson', UploadJson),
    ('/api/manifest/addmanifest/(\d+)', AddManifest),
    ('/upload/manifest', UploadManifestPage)
], debug=True)
