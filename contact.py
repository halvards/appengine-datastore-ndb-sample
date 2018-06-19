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

"""Models for representing a contact with multiple nested data structures."""


from google.appengine.ext import ndb


class Address(ndb.Model):
    """A model representing a structured address."""
    street = ndb.StringProperty()
    suburb = ndb.StringProperty()
    state = ndb.StringProperty(
        choices=('ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'))
    postcode = ndb.StringProperty()


class PhoneNumber(ndb.Model):
    """A model representing a structured phone number."""
    phone_type = ndb.StringProperty(
        choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = ndb.StringProperty()


class Contact(ndb.Model):
    """A Contact model that uses ndb.StructuredProperty for nested data."""
    name = ndb.StringProperty()
    address = ndb.StructuredProperty(Address)
    phone_numbers = ndb.StructuredProperty(PhoneNumber, repeated=True)
    labels = ndb.JsonProperty()  # this means labels can be any structure
