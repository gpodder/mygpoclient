# -*- coding: utf-8 -*-
# gpodder.net API Client
# Copyright (C) 2009-2010 Thomas Perl
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

from mygpoclient import http
from mygpoclient import json

import unittest
import minimock

class Test_JsonClient(unittest.TestCase):
    USERNAME = 'john'
    PASSWORD = 'secret'

    def setUp(self):
        self.client = json.JsonClient(self.USERNAME, self.PASSWORD)

    def tearDown(self):
        minimock.restore()

    def mock_setHttpResponse(self, value):
        http.HttpClient._request = minimock.Mock('http.HttpClient._request')
        http.HttpClient._request.mock_returns = value

    def test_parseResponse_worksWithDictionary(self):
        self.mock_setHttpResponse('{"a": "B", "c": "D"}')
        items = list(sorted(self.client.GET('/').items()))
        self.assertEquals(items, [('a', 'B'), ('c', 'D')])

    def test_parseResponse_worksWithIntegerList(self):
        self.mock_setHttpResponse('[1,2,3,6,7]')
        self.assertEquals(self.client.GET('/'), [1,2,3,6,7])

    def test_parseResponse_emptyString_returnsNone(self):
        self.mock_setHttpResponse('')
        self.assertEquals(self.client.GET('/'), None)

    def test_invalidContent_raisesJsonException(self):
        self.mock_setHttpResponse('this is not a valid json string')
        self.assertRaises(json.JsonException, self.client.GET, '/')


