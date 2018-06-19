# Copyright 2018 Google LLC
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

import logging
import ujson
from contact import Contact
from flask import Flask, request, Response
from google.appengine.ext import ndb


app = Flask(__name__)


@app.route('/')
def hello():
    resp = Response('Hello World!', 200)
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/contacts', methods=['GET'])
def get_contact():
    contact_urlsafe_key = request.args.get('contact_id')
    logging.info('Looking up Contact using key %s', contact_urlsafe_key)
    contact_key = ndb.Key(urlsafe=contact_urlsafe_key)
    contact = contact_key.get()
    contact_json = ujson.dumps(contact.to_dict())
    resp = Response(contact_json, 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/contacts', methods=['POST'])
def create_contact():
    request_data = request.get_data(as_text=True)
    logging.info('Creating contact from JSON: %s', request_data)

    contact_dict = ujson.loads(request_data)
    contact = Contact(**contact_dict)
    contact_key = contact.put()

    logging.info('Created contact %s with urlsafe key %s',
                 contact.name, contact_key.urlsafe())

    resp = Response('', 204)
    resp.headers['Location'] = (request.base_url +
                                '?contact_id=' +
                                contact_key.urlsafe())
    return resp


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    resp = Response("An internal error occurred.", 500)
    resp.headers['Content-Type'] = 'text/plain'
    return resp
