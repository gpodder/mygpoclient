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

from mygpoclient import locator
from mygpoclient import json

class SimpleClient(object):
    """Client for the my.gpodder.org Simple API

    This is the API client implementation that provides a
    pythonic interface to the my.gpodder.org Simple API.
    """
    FORMAT = 'json'

    def __init__(self, username, password, host=mygpoclient.HOST):
        """Creates a new Simple API client

        Username and password must be specified and are
        the user's login data for the webservice.

        The parameter host is optional and defaults to
        the main webservice.
        """
        self.username = username
        self.password = password
        self._locator = locator.Locator(username, host)
        self._client = json.JsonClient(username, password)

    def get_subscriptions(self, device_id):
        """Get a list of subscriptions for a device

        Returns a list of URLs (one per subscription) for
        the given device_id that reflects the current list
        of subscriptions.

        Raises http.NotFound if the device does not exist.
        """
        uri = self._locator.subscriptions_uri(device_id, self.FORMAT)
        return self._client.GET(uri)

    def put_subscriptions(self, device_id, urls):
        """Update a device's subscription list

        Sets the server-side subscription list for the device
        "device_id" to be equivalent to the URLs in the list of
        strings "urls".

        The device will be created if it does not yet exist.

        Returns True if the update was successful, False otherwise.
        """
        uri = self._locator.subscriptions_uri(device_id, self.FORMAT)
        return (self._client.PUT(uri, urls) == None)

