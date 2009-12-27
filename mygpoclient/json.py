# -*- coding: utf-8 -*-
# my.gpodder.org API Client
# Copyright (C) 2009 Thomas Perl
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

import mygpoclient

import simplejson as json

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

    def encode(self, data):
        """Encodes a object into its JSON string repesentation

        >>> client = JsonClient()
        >>> client.encode(None)
        ''
        >>> client.encode([1,2,3])
        '[1, 2, 3]'
        >>> client.encode(42)
        '42'
        """
        if data is None:
            return ''
        else:
            return json.dumps(data)

    def decode(self, data):
        """Decodes a response string to a Python object

        >>> client = JsonClient()
        >>> client.decode('')
        >>> client.decode('[1,2,3]')
        [1, 2, 3]
        >>> client.decode('42')
        42
        """
        if data == '':
            return None
        else:
            try:
                return json.loads(data)
            except ValueError, ve:
                raise JsonException('Value error while parsing response: ' + data)

    def _request(self, method, uri, data):
        data = self.encode(data)
        response = http.HttpClient._request(self, method, uri, data)
        return self.decode(response)

