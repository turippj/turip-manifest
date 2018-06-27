import os
import json
import webapp2
import jinja2
from collections import OrderedDict
from google.appengine.ext import ndb
from google.appengine.api import search

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# [ Start DataTemplate ]
class DataTemplate(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()


# [ End DataTemplate ]


# [ Start Interface ]
class Interface(ndb.Model):
    type = ndb.StringProperty()

    # [START query]
    @classmethod
    def query_interface(cls):
        return cls.query().order()
    # [END query]


# [ Start Interface ]


# [ Start Manifest ]
class Manifest(DataTemplate):
    protocol = ndb.StringProperty()
    model = ndb.IntegerProperty()
    interface = ndb.KeyProperty(kind=Interface, repeated=True)

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
                        type=content['type']
                        )
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

        interface_string = data.get('interface')
        interfaces = []
        for interface in interface_string:
            existing_interface = Interface.query(Interface.type == interface).get()
            if existing_interface is None:
                new_interface = Interface(type=interface)
                interfaces.append(new_interface.put())
            else:
                interfaces.append(existing_interface.key)

        if data.get('name') is None or data.get('description') is None or data.get('protocol') is None or data.get(
                'port') is None:
            self.response.write('Your Manifest Data is not correct.')

        else:
            manifest = Manifest(model=model_number,
                                name=data['name'],
                                description=data['description'],
                                protocol=data['protocol'])

            for interface in interfaces:
                manifest.interface.append(interface)

            document = search.Document(
                fields=[
                    search.TextField(name='model', value=hex(model_number).replace('0x', '')),
                    search.TextField(name='name', value=data['name']),
                    search.TextField(name='description', value=data['description']),
                    search.TextField(name='protocol', value=data['protocol']),
                ])
            index = search.Index('manifest')

            index.put(document)
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


# [ Start SearchManifestByNumber ]
class SearchManifestByNumber(webapp2.RequestHandler):
    def get(self, model):
        manifest = Manifest.query(Manifest.model == long(model, 16)).get()
        if manifest is None:
            self.response.write("404")
        else:
            output_data = OrderedDict()
            output_data['model'] = hex(manifest.model).replace('0x', '')
            output_data['name'] = manifest.name
            output_data['interface'] = manifest.interface
            output_data['description'] = manifest.description
            output_data['interface'] = []
            output_data['port'] = []

            for interface in manifest.interface:
                interface_data = interface.get()
                output_data['interface'].append(interface_data.type)

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

# [ Start SearchManifestByKeyword ]
class SearchManifestByKeyword(webapp2.RequestHandler):
    def get(self):
        category = self.request.get("category")
        keyword = self.request.get("keyword")

        index = search.Index('manifest')
        query_string = category + ': ' + keyword

        results = index.search(query_string)
        searchResults = []

        for result in results:
            datas = {}
            for data in result.fields:
                datas[data.name.encode('utf-8')] = data.value.encode('utf-8')
            searchResults.append(datas)
        self.response.write(json.dumps(searchResults))


# [ End SearchManifestByKeyword ]

# [ Start AddManifestPage ]
class UploadManifestPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('manifest.html')
        self.response.write(template.render())


# [ End AddManifestPage ]


class DeleteIndex(webapp2.RequestHandler):
    def get(self):
        document_id = self.request.get("document_id")
        index = search.Index('manifest')
        index.delete(document_id)
        self.response.write('Delete success!')


app = webapp2.WSGIApplication([
    ('/api/manifest/add', AddManifest),
    ('/api/manifest/search', SearchManifestByKeyword),
    ('/api/search/delete', DeleteIndex),
    ('/manifest/upload', UploadManifestPage),
    ('/(\w+)', SearchManifestByNumber)
], debug=True)
