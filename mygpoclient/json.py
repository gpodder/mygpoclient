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

    def _request(self, method, uri, data):
        data = json.dumps(data)
        response = http.HttpClient._request(self, method, uri, data)
        try:
            response = json.loads(response)
        except ValueError, ve:
            raise JsonException('Value error while parsing response')
        return response

