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

try:
    # Python 3
    from io import BytesIO
    from urllib import request

except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO
    import urllib2 as request

from mygpoclient import http
from mygpoclient import json

import unittest
import minimock


def fqname(o):
      return o.__module__ + "." + o.__name__

class Test_JsonClient(unittest.TestCase):
    PORT = 9876
    URI_BASE = 'http://localhost:%(PORT)d' % locals()
    USERNAME = 'john'
    PASSWORD = 'secret'

    @classmethod
    def setUpClass(cls):
        cls.odName = fqname(request.OpenerDirector)
        cls.boName = fqname(request.build_opener)

    def setUp(self):
        self.mockopener = minimock.Mock(self.odName)
        request.build_opener = minimock.Mock(self.boName)
        request.build_opener.mock_returns = self.mockopener

    def tearDown(self):
        minimock.restore()

    def mock_setHttpResponse(self, value):
        self.mockopener.open.mock_returns = BytesIO(value)

    def test_parseResponse_worksWithDictionary(self):
        client = json.JsonClient(self.USERNAME, self.PASSWORD)
        self.mock_setHttpResponse(b'{"a": "B", "c": "D"}')
        items = list(sorted(client.GET(self.URI_BASE + '/').items()))
        self.assertEquals(items, [('a', 'B'), ('c', 'D')])

    def test_parseResponse_worksWithIntegerList(self):
        client = json.JsonClient(self.USERNAME, self.PASSWORD)
        self.mock_setHttpResponse(b'[1,2,3,6,7]')
        self.assertEquals(client.GET(self.URI_BASE + '/'), [1,2,3,6,7])

    def test_parseResponse_emptyString_returnsNone(self):
        client = json.JsonClient(self.USERNAME, self.PASSWORD)
        self.mock_setHttpResponse(b'')
        self.assertEquals(client.GET(self.URI_BASE + '/'), None)

    def test_invalidContent_raisesJsonException(self):
        client = json.JsonClient(self.USERNAME, self.PASSWORD)
        self.mock_setHttpResponse(b'this is not a valid json string')
        self.assertRaises(json.JsonException, client.GET, self.URI_BASE + '/')


