# appengine-datastore-ndb-sample

This is a sample application for
[Google App Engine Python Standard Environment](https://cloud.google.com/appengine/docs/standard/python/)
using
[Google Cloud Datastore](https://cloud.google.com/datastore/docs/concepts/overview)
and the
[Python NDB Client Library](https://cloud.google.com/appengine/docs/standard/python/ndb/).

It demonstrates how to use Cloud Datastore entities with nested models and how
to map this to a simple HTTP JSON API.

The Contacts model (see `contact.py`) has multiple examples of nested
structures:

- Properties that can only have values from a predefined list (enum), using
  `choice`, (see `state` in the `Address` class and `phone_type` in the
  `PhoneNumber` class).
- Nested data with known structure using `ndb.StructuredProperty`
  (see `address` in the `Contact` class).
- Repeated data (array) with structure using `ndb.StructuredProperty` and
  `repeated=True` (see `phone_numbers` in the `Contact` class).
- Nested data with arbitrary structure using `ndb.JsonProperty` (see `labels`
  in the `Contact` class).

## Run the application

Set up virtualenv:

    virtualenv -p python2.7 env
    source env/bin/activate

Install dependencies:

    pip install -t lib -r requirements.txt

The sample application can be run using either the Local Development Server or
by deploying to App Engine.

### Local Development Server

Install dependencies that are bundled with App Engine but not by the Local
Development Server:

    pip install -r requirements-dev.txt

Run the application locally, on `http://localhost:8080/`:

    dev_appserver.py app.yaml
    
### App Engine
    
Deploy the application to App Engine, on `https://[PROJECT_ID].appspot.com/`:

    gcloud app deploy app.yaml -q
    
## Usage

Interact with the API using `curl` or your favorite HTTP client.

Create a contact from a JSON file:

    curl -vX POST -H "Content-Type: application/json" -d @test_contact.json http://localhost:8080/contacts

Create a contact from a JSON string:

    curl -vX POST -H "Content-Type: application/json" -d '{"name":"String Person","address":{"state":"VIC","street":"2 Other Avenue","suburb":"Melbourne","postcode":"3000"},"phone_numbers":[{"number":"0223456789","phone_type":"home"},{"number":"0498765432","phone_type":"mobile"}],"labels":{"label1":"label1 value","label3":"label3 value"}}' http://localhost:8080/contacts

The `Location` header of the response shows the URL that can be used to
retrieve the newly created contact.

Retrieve a contact:

    curl -s http://localhost:8080/contacts?contact_id=[CONTACT_ID] | python -m json.tool

## Authentication

This sample application doesn't include any authentication. If you deploy to
App Engine you should enable
[Cloud Identity-Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview)
for your application. You can do this from the
[Google Cloud Platform console](https://console.cloud.google.com/security/iap/).

## Disclaimer

This is not an officially supported Google product.
