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

import webapp2
from google.appengine.ext import ndb


# [ Start DataTemplate ]s
class DataTemplate(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
# [ End DataTemplate ]


# [ Start Manifest ]
class Manifest(DataTemplate):
    model_number = ndb.IntegerProperty()
    author = ndb.StringProperty()

    # [ port methods ]
    def add(self, content):
        port = Port(parent=self.key,
                    port_number=content['port_number'],
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
    port_number = ndb.IntegerProperty()
    permission = ndb.StringProperty()
    type = ndb.StringProperty()
# [ End Port ]


# [ Start AddManifest ]
class AddManifest(webapp2.RequestHandler):
    def post(self):
        model_number = 65535  # The first free model_number
        existing_manifest = Manifest.query(Manifest.model_number == model_number).get()
        while existing_manifest is not None:
            model_number += 1
            existing_manifest = Manifest.query(Manifest.model_number == model_number).get()

        name = self.request.get('name')
        description = self.request.get('description')
        author = self.request.get('author')
        manifest = Manifest(
                    model_number=model_number,
                    name=name,
                    description=description,
                    author=author)
        manifest.put()
# [ End AddManifest ]


# [ Start AddPort ]
class AddPort(webapp2.RequestHandler):
    def post(self, model_id):
        manifest = Manifest.get_by_id(model_id)
        content = {'port_number': self.request.get('port_number'),
                   'name': self.request.get('name'),
                   'description': self.request.get('description'),
                   'permission': self.request.get('permission'),
                   'type': self.request.get('type')}
        manifest.add(content)
# [ End AddPort ]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/manifest/addmanifest', AddManifest),
    ('/api/manifest/addport', AddPort)
], debug=True)
