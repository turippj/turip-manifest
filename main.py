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
from collections import OrderedDict
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

    # [ port methods ]
    def add(self, content):
        if content.get('number') is None or content.get('name') is None or \
           content.get('description') is None or content.get('permission') is None or content.get('type') is None:
            return -1
        else:
            port = Port(parent=self.key,
                        number=content['number'],
                        name=content['name'],
                        description=content['description'],
                        permission=content['permission'],
                        type=content['type'])
            port.put()
            return 0


# [ End Manifest ]


# [ Start Port ]
class Port(DataTemplate):
    number = ndb.IntegerProperty()
    permission = ndb.StringProperty()
    type = ndb.StringProperty()
# [ End Port ]


# [ Start AddManifest ]
class AddManifest(webapp2.RequestHandler):
    def post(self):
        json_file = str(self.request.get('file_data'))
        data = json.loads(json_file)

        model_number = 65535  # The first free model_number
        existing_manifest = Manifest.query(Manifest.model == model_number).get()
        while existing_manifest is not None:
            model_number += 1
            existing_manifest = Manifest.query(Manifest.model == model_number).get()

        if data.get('name') is None or data.get('description') is None or data.get('author') is None or data.get('port') is None:
            self.response.write('Your Manifest Data is not correct.')
        else:
            manifest = Manifest(
                        model=model_number,
                        name=data['name'],
                        description=data['description'],
                        author=data['author'])
            manifest.put()
            for port in data['port']:
                if manifest.add(port) != 0:
                    ports = Port.query(ancestor=manifest.key).fetch()
                    if ports is not None:
                        for num in range(len(ports)):
                            ports[num].key.delete()
                    manifest.key.delete()
                    self.response.write('Your Manifest Data is not correct.')
                    return
            self.response.write('Upload Manifest success!')
# [ End AddManifest ]


# [ Start SearchManifest ]
class SearchManifest(webapp2.RequestHandler):
    def get(self, model):
        manifest = Manifest.query(Manifest.model == long(model)).get()
        if manifest is None:
            self.response.write("404 Manifest is not found.")

        output_data = OrderedDict()
        output_data['model'] = manifest.model
        output_data['name'] = manifest.name
        output_data['author'] = manifest.author
        output_data['description'] = manifest.description
        output_data['port'] = []

        ports = Port.query(ancestor=manifest.key).order(Port.number).fetch()

        for num in range(len(ports)):
            port = OrderedDict()
            port['number'] = ports[num].number
            port['name'] = ports[num].name
            port['description'] = ports[num].description
            port['permission'] = ports[num].permission
            port['type'] = ports[num].type

            output_data['port'].append(port)

        output_json = json.dumps(output_data)
        self.response.write(output_json)
# [ End SearchManifest ]


# [ Start AddManifestPage ]
class UploadManifestPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('manifest.html')
        self.response.write(template.render())
# [ End AddManifestPage ]


app = webapp2.WSGIApplication([
    ('/api/manifest/add_manifest', AddManifest),
    ('/api/manifest/search_manifest/(\d+)', SearchManifest),
    ('/upload/manifest', UploadManifestPage)
], debug=True)
