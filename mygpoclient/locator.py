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

import mygpoclient

import os

try:
    # Python 3
    from urllib.parse import quote_plus, quote

except ImportError:
    # Python 2
    from urllib import quote_plus, quote

from mygpoclient import util

class Locator(object):
    """URI Locator for API endpoints

    This helper class abstracts the URIs for the gpodder.net
    webservice and provides a nice facility for generating API
    URIs and checking parameters.
    """
    SIMPLE_FORMATS = ('opml', 'json', 'txt')

    SETTINGS_TYPES = ('account', 'device', 'podcast', 'episode')

    def __init__(self, username, root_url=mygpoclient.ROOT_URL,
            version=mygpoclient.VERSION):
        self._username = username
        if root_url.endswith('/'):
            root_url = root_url[:-1]
        if root_url.startswith('http'):
            self._simple_base = root_url
            self._base = '%(root_url)s/api/%(version)s' % locals()
        else:
            self._simple_base = 'http://%(root_url)s' % locals()
            self._base = 'http://%(root_url)s/api/%(version)s' % locals()

    def _convert_since(self, since):
        """Convert "since" into a numeric value

        This is internally used for value-checking.
        """
        try:
            return int(since)
        except ValueError:
            raise ValueError('since must be a numeric value (or None)')

    def subscriptions_uri(self, device_id=None, format='opml'):
        """Get the Simple API URI for a subscription list

        >>> locator = Locator('john')
        >>> locator.subscriptions_uri('n800')
        'http://gpodder.net/subscriptions/john/n800.opml'
        >>> locator.subscriptions_uri('ipod', 'txt')
        'http://gpodder.net/subscriptions/john/ipod.txt'
        """
        if format not in self.SIMPLE_FORMATS:
            raise ValueError('Unsupported file format')

        username = self._username
        if device_id is None:
            path = '%(username)s.%(format)s' % locals()
        else:
            path = '%(username)s/%(device_id)s.%(format)s' % locals()
        return util.join(self._simple_base,
                'subscriptions', path)

    def toplist_uri(self, count=50, format='opml'):
        """Get the Simple API URI for the toplist

        >>> locator = Locator(None)
        >>> locator.toplist_uri()
        'http://gpodder.net/toplist/50.opml'
        >>> locator.toplist_uri(70)
        'http://gpodder.net/toplist/70.opml'
        >>> locator.toplist_uri(10, 'json')
        'http://gpodder.net/toplist/10.json'
        """
        if format not in self.SIMPLE_FORMATS:
            raise ValueError('Unsupported file format')

        filename = 'toplist/%(count)d.%(format)s' % locals()
        return util.join(self._simple_base, filename)

    def suggestions_uri(self, count=10, format='opml'):
        """Get the Simple API URI for user suggestions

        >>> locator = Locator('john')
        >>> locator.suggestions_uri()
        'http://gpodder.net/suggestions/10.opml'
        >>> locator.suggestions_uri(50)
        'http://gpodder.net/suggestions/50.opml'
        >>> locator.suggestions_uri(70, 'json')
        'http://gpodder.net/suggestions/70.json'
        """
        if format not in self.SIMPLE_FORMATS:
            raise ValueError('Unsupported file format')

        filename = 'suggestions/%(count)d.%(format)s' % locals()
        return util.join(self._simple_base, filename)

    def search_uri(self, query, format='opml'):
        """Get the Simple API URI for podcast search

        >>> locator = Locator(None)
        >>> locator.search_uri('outlaws')
        'http://gpodder.net/search.opml?q=outlaws'
        >>> locator.search_uri(':something?', 'txt')
        'http://gpodder.net/search.txt?q=%3Asomething%3F'
        >>> locator.search_uri('software engineering', 'json')
        'http://gpodder.net/search.json?q=software+engineering'
        """
        if format not in self.SIMPLE_FORMATS:
            raise ValueError('Unsupported file format')

        query = quote_plus(query)
        filename = 'search.%(format)s?q=%(query)s' % locals()
        return util.join(self._simple_base, filename)

    def add_remove_subscriptions_uri(self, device_id):
        """Get the Advanced API URI for uploading list diffs

        >>> locator = Locator('bill')
        >>> locator.add_remove_subscriptions_uri('n810')
        'http://gpodder.net/api/2/subscriptions/bill/n810.json'
        """
        filename = '%(device_id)s.json' % locals()
        return util.join(self._base,
                'subscriptions', self._username, filename)

    def subscription_updates_uri(self, device_id, since=None):
        """Get the Advanced API URI for downloading list diffs

        The parameter "since" is optional and should be a numeric
        value (otherwise a ValueError is raised).

        >>> locator = Locator('jen')
        >>> locator.subscription_updates_uri('n900')
        'http://gpodder.net/api/2/subscriptions/jen/n900.json'
        >>> locator.subscription_updates_uri('n900', 1234)
        'http://gpodder.net/api/2/subscriptions/jen/n900.json?since=1234'
        """
        filename = '%(device_id)s.json' % locals()
        if since is not None:
            since = self._convert_since(since)
            filename += '?since=%(since)d' % locals()

        return util.join(self._base,
                'subscriptions', self._username, filename)

    def upload_episode_actions_uri(self):
        """Get the Advanced API URI for uploading episode actions

        >>> locator = Locator('thp')
        >>> locator.upload_episode_actions_uri()
        'http://gpodder.net/api/2/episodes/thp.json'
        """
        filename = self._username + '.json'
        return util.join(self._base, 'episodes', filename)

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
        'http://gpodder.net/api/2/episodes/steve.json'
        >>> locator.download_episode_actions_uri(since=1337)
        'http://gpodder.net/api/2/episodes/steve.json?since=1337'
        >>> locator.download_episode_actions_uri(podcast='http://example.org/episodes.rss')
        'http://gpodder.net/api/2/episodes/steve.json?podcast=http%3A//example.org/episodes.rss'
        >>> locator.download_episode_actions_uri(since=2000, podcast='http://example.com/')
        'http://gpodder.net/api/2/episodes/steve.json?since=2000&podcast=http%3A//example.com/'
        >>> locator.download_episode_actions_uri(device_id='ipod')
        'http://gpodder.net/api/2/episodes/steve.json?device=ipod'
        >>> locator.download_episode_actions_uri(since=54321, device_id='ipod')
        'http://gpodder.net/api/2/episodes/steve.json?since=54321&device=ipod'
        """
        if podcast is not None and device_id is not None:
            raise ValueError('must not specify both "podcast" and "device_id"')

        filename = self._username + '.json'

        params = []
        if since is not None:
            since = str(self._convert_since(since))
            params.append(('since', since))

        if podcast is not None:
            params.append(('podcast', podcast))

        if device_id is not None:
            params.append(('device', device_id))

        if params:
            filename += '?' + '&'.join('%s=%s' % (key, quote(value)) for key, value in params)

        return util.join(self._base, 'episodes', filename)

    def device_settings_uri(self, device_id):
        """Get the Advanced API URI for setting per-device settings uploads

        >>> locator = Locator('mike')
        >>> locator.device_settings_uri('ipod')
        'http://gpodder.net/api/2/devices/mike/ipod.json'
        """
        filename = '%(device_id)s.json' % locals()
        return util.join(self._base, 'devices', self._username, filename)

    def device_list_uri(self):
        """Get the Advanced API URI for retrieving the device list

        >>> locator = Locator('jeff')
        >>> locator.device_list_uri()
        'http://gpodder.net/api/2/devices/jeff.json'
        """
        filename = self._username + '.json'
        return util.join(self._base, 'devices', filename)

    def toptags_uri(self, count=50):
        """Get the Advanced API URI for retrieving the top Tags

        >>> locator = Locator(None)
        >>> locator.toptags_uri()
        'http://gpodder.net/api/2/tags/50.json'
        >>> locator.toptags_uri(70)
        'http://gpodder.net/api/2/tags/70.json'
        """
        filename = '%(count)d.json' % locals()
        return util.join(self._base, 'tags', filename)

    def podcasts_of_a_tag_uri(self, tag, count=50):
        """Get the Advanced API URI for retrieving the top Podcasts of a Tag

        >>> locator = Locator(None)
        >>> locator.podcasts_of_a_tag_uri('linux')
        'http://gpodder.net/api/2/tag/linux/50.json'
        >>> locator.podcasts_of_a_tag_uri('linux',70)
        'http://gpodder.net/api/2/tag/linux/70.json'
        """
        filename = '%(tag)s/%(count)d.json' % locals()
        return util.join(self._base, 'tag', filename)

    def podcast_data_uri(self, podcast_url):
        """Get the Advanced API URI for retrieving Podcast Data

        >>> locator = Locator(None)
        >>> locator.podcast_data_uri('http://podcast.com')
        'http://gpodder.net/api/2/data/podcast.json?url=http%3A//podcast.com'
        """
        filename = 'podcast.json?url=%s' % quote(podcast_url)
        return util.join(self._base, 'data', filename)

    def episode_data_uri(self, podcast_url, episode_url):
        """Get the Advanced API URI for retrieving Episode Data

        >>> locator = Locator(None)
        >>> locator.episode_data_uri('http://podcast.com','http://podcast.com/foo')
        'http://gpodder.net/api/2/data/episode.json?podcast=http%3A//podcast.com&url=http%3A//podcast.com/foo'
        """
        filename = 'episode.json?podcast=%s&url=%s' % (quote(podcast_url), quote(episode_url))
        return util.join(self._base, 'data', filename)

    def favorite_episodes_uri(self):
        """Get the Advanced API URI for listing favorite episodes

        >>> locator = Locator('mike')
        >>> locator.favorite_episodes_uri()
        'http://gpodder.net/api/2/favorites/mike.json'
        """
        filename = self._username + '.json'
        return util.join(self._base, 'favorites', filename)

    def settings_uri(self, type, scope_param1, scope_param2):
        """Get the Advanced API URI for retrieving or saving Settings

        Depending on the Type of setting scope_param2 or scope_param1 and scope_param2 are
        not necessary.

        >>> locator = Locator('joe')
        >>> locator.settings_uri('account',None,None)
        'http://gpodder.net/api/2/settings/joe/account.json'
        >>> locator.settings_uri('device','foodevice',None)
        'http://gpodder.net/api/2/settings/joe/device.json?device=foodevice'
        >>> locator.settings_uri('podcast','http://podcast.com',None)
        'http://gpodder.net/api/2/settings/joe/podcast.json?podcast=http%3A//podcast.com'
        >>> locator.settings_uri('episode','http://podcast.com','http://podcast.com/foo')
        'http://gpodder.net/api/2/settings/joe/episode.json?podcast=http%3A//podcast.com&episode=http%3A//podcast.com/foo'
        """
        if type not in self.SETTINGS_TYPES:
            raise ValueError('Unsupported Setting Type')

        filename = self._username + '/%(type)s.json' % locals()

        if type == 'device':
            if scope_param1 is None:
                raise ValueError('Devicename not specified')
            filename += '?device=%(scope_param1)s' % locals()

        if type == 'podcast':
            if scope_param1 is None:
                raise ValueError('Podcast URL not specified')
            filename += '?podcast=%s' % quote(scope_param1)

        if type == 'episode':
            if (scope_param1 is None) or (scope_param2 is None):
                raise ValueError('Podcast or Episode URL not specified')
            filename += '?podcast=%s&episode=%s' % (quote(scope_param1), quote(scope_param2))

        return util.join(self._base, 'settings' , filename)

    def root_uri(self):
        """ Get the server's root URI.

        >>> locator = Locator(None)
        >>> locator.root_uri()
        'http://gpodder.net'
        """
        return self._simple_base
