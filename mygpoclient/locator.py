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

import os
import urllib

class Locator(object):
    """URI Locator for API endpoints

    This helper class abstracts the URIs for the my.gpodder.org
    webservice and provides a nice facility for generating API
    URIs and checking parameters.
    """
    SIMPLE_FORMATS = ('opml', 'json', 'txt')

    def __init__(self, username, host=mygpoclient.HOST,
            version=mygpoclient.VERSION):
        self._username = username
        self._simple_base = 'http://%(host)s' % locals()
        self._base = 'http://%(host)s/api/%(version)s' % locals()

    def _convert_since(self, since):
        """Convert "since" into a numeric value

        This is internally used for value-checking.
        """
        try:
            return int(since)
        except ValueError:
            raise ValueError('since must be a numeric value (or None)')

    def subscriptions_uri(self, device_id, format='opml'):
        """Get the Simple API URI for a subscription list

        >>> locator = Locator('john')
        >>> locator.subscriptions_uri('n800')
        'http://my.gpodder.org/subscriptions/john/n800.opml'
        >>> locator.subscriptions_uri('ipod', 'txt')
        'http://my.gpodder.org/subscriptions/john/ipod.txt'
        """
        if format not in self.SIMPLE_FORMATS:
            raise ValueError('Unsupported file format')

        filename = '%(device_id)s.%(format)s' % locals()
        return os.path.join(self._simple_base,
                'subscriptions', self._username, filename)

    def add_remove_subscriptions_uri(self, device_id):
        """Get the Advanced API URI for uploading list diffs

        >>> locator = Locator('bill')
        >>> locator.add_remove_subscriptions_uri('n810')
        'http://my.gpodder.org/api/1/subscriptions/bill/n810.json'
        """
        filename = '%(device_id)s.json' % locals()
        return os.path.join(self._base,
                'subscriptions', self._username, filename)

    def subscription_updates_uri(self, device_id, since=None):
        """Get the Advanced API URI for downloading list diffs

        The parameter "since" is optional and should be a numeric
        value (otherwise a ValueError is raised).

        >>> locator = Locator('jen')
        >>> locator.subscription_updates_uri('n900')
        'http://my.gpodder.org/api/1/subscriptions/jen/n900.json'
        >>> locator.subscription_updates_uri('n900', 1234)
        'http://my.gpodder.org/api/1/subscriptions/jen/n900.json?since=1234'
        """
        filename = '%(device_id)s.json' % locals()
        if since is not None:
            since = self._convert_since(since)
            filename += '?since=%(since)d' % locals()

        return os.path.join(self._base,
                'subscriptions', self._username, filename)

    def upload_episode_actions_uri(self):
        """Get the Advanced API URI for uploading episode actions

        >>> locator = Locator('thp')
        >>> locator.upload_episode_actions_uri()
        'http://my.gpodder.org/api/1/episodes/thp.json'
        """
        filename = self._username + '.json'
        return os.path.join(self._base, 'episodes', filename)

    def download_episode_actions_uri(self, since=None,
            podcast=None, device_id=None):
        """Get the Advanced API URI for downloading episode actions

        The parameter "since" is optional and should be a numeric
        value (otherwise a ValueError is raised).

        Both "podcast" and "device_id" are optional and exclusive:

            "podcast" should be a podcast URL
            "device_id" should be a device ID

        >>> locator = Locator('steve')
        >>> locator.download_episode_actions_uri()
        'http://my.gpodder.org/api/1/episodes/steve.json'
        >>> locator.download_episode_actions_uri(since=1337)
        'http://my.gpodder.org/api/1/episodes/steve.json?since=1337'
        >>> locator.download_episode_actions_uri(podcast='http://example.org/episodes.rss')
        'http://my.gpodder.org/api/1/episodes/steve.json?podcast=http%3A//example.org/episodes.rss'
        >>> locator.download_episode_actions_uri(since=2000, podcast='http://example.com/')
        'http://my.gpodder.org/api/1/episodes/steve.json?since=2000&podcast=http%3A//example.com/'
        >>> locator.download_episode_actions_uri(device_id='ipod')
        'http://my.gpodder.org/api/1/episodes/steve.json?device=ipod'
        >>> locator.download_episode_actions_uri(since=54321, device_id='ipod')
        'http://my.gpodder.org/api/1/episodes/steve.json?since=54321&device=ipod'
        """
        if podcast is not None and device_id is not None:
            raise ValueError('must not specify both "podcast" and "device_id"')

        filename = self._username+'.json'

        params = []
        if since is not None:
            since = str(self._convert_since(since))
            params.append(('since', since))

        if podcast is not None:
            params.append(('podcast', podcast))

        if device_id is not None:
            params.append(('device', device_id))

        if params:
            filename += '?' + '&'.join('%s=%s' % (key, urllib.quote(value)) for key, value in params)

        return os.path.join(self._base, 'episodes', filename)

    def device_settings_uri(self, device_id):
        """Get the Advanced API URI for setting per-device settings uploads

        >>> locator = Locator('mike')
        >>> locator.device_settings_uri('ipod')
        'http://my.gpodder.org/api/1/devices/mike/ipod.json'
        """
        filename = '%(device_id)s.json' % locals()
        return os.path.join(self._base, 'devices', self._username, filename)

    def device_list_uri(self):
        """Get the Advanced API URI for retrieving the device list

        >>> locator = Locator('jeff')
        >>> locator.device_list_uri()
        'http://my.gpodder.org/api/1/devices/jeff.json'
        """
        filename = self._username + '.json'
        return os.path.join(self._base, 'devices', filename)


