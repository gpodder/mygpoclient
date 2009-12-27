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

from mygpoclient import http
from mygpoclient import simple

import unittest
import minimock

class Test_SimpleClient(unittest.TestCase):
    USERNAME = 'a'
    PASSWORD = 'b'
    DEVICE_NAME = 'x'
    SUBSCRIPTIONS = [
            'http://lugradio.org/episodes.rss',
            'http://feeds2.feedburner.com/LinuxOutlaws',
    ]
    SUBSCRIPTIONS_JSON = """
      ["http://lugradio.org/episodes.rss",
       "http://feeds2.feedburner.com/LinuxOutlaws"]
    """

    def setUp(self):
        self.client = simple.SimpleClient(self.USERNAME, self.PASSWORD)

    def tearDown(self):
        minimock.restore()

    def mock_setHttpResponse(self, value):
        http.HttpClient._request = minimock.Mock('http.HttpClient._request')
        http.HttpClient._request.mock_returns = value

    def test_putSubscriptions(self):
        self.mock_setHttpResponse('')
        result = self.client.put_subscriptions(self.DEVICE_NAME, self.SUBSCRIPTIONS)
        self.assertEquals(result, True)

    def test_getSubscriptions(self):
        self.mock_setHttpResponse(self.SUBSCRIPTIONS_JSON)
        subscriptions = self.client.get_subscriptions(self.DEVICE_NAME)
        self.assertEquals(subscriptions, self.SUBSCRIPTIONS)

