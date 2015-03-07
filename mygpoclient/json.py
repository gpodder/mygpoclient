# -*- coding: utf-8 -*-
# gpodder.net API Client
# Copyright (C) 2009-2013 Thomas Perl and the gPodder Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Fix gPodder bug 900 (so "import json" doesn't import this module)
from __future__ import absolute_import

import mygpoclient

try:
    # Python 3
    bytes = bytes

except:
    # Python 2
    bytes = str

import json

from mygpoclient import http

# Additional exceptions for JSON-related errors
class JsonException(Exception): pass

class JsonClient(http.HttpClient):
    """A HttpClient with built-in JSON support

    This client will automatically marshal and unmarshal data for
    JSON-related web services so that code using this class will
    not need to care about (de-)serialization of data structures.
    """
    def __init__(self, username=None, password=None):
        http.HttpClient.__init__(self, username, password)

    @staticmethod
    def encode(data):
        """Encodes a object into its JSON string repesentation

        >>> JsonClient.encode(None) is None
        True
        >>> JsonClient.encode([1,2,3]) == b'[1, 2, 3]'
        True
        >>> JsonClient.encode(42) == b'42'
        True
        """
        if data is None:
            return None
        else:
            return json.dumps(data).encode('utf-8')

    @staticmethod
    def decode(data):
        """Decodes a response string to a Python object

        >>> JsonClient.decode(b'')
        >>> JsonClient.decode(b'[1,2,3]')
        [1, 2, 3]
        >>> JsonClient.decode(b'42')
        42
        """
        if data == b'':
            return None

        data = data.decode('utf-8')
        try:
            return json.loads(data)
        except ValueError:
            raise JsonException('Value error while parsing response: ' + data)

    @staticmethod
    def _prepare_request(method, uri, data):
        data = JsonClient.encode(data)
        return http.HttpClient._prepare_request(method, uri, data)

    @staticmethod
    def _process_response(response):
        data = http.HttpClient._process_response(response)
        return JsonClient.decode(data)
