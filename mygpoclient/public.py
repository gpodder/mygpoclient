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

from mygpoclient import locator
from mygpoclient import json
from mygpoclient import simple

class Tag(object):
    """Container class for a tag in the top tag list

    Attributes:
    tag - The name of the tag
    usage - Usage of the tag
    """

    REQUIRED_KEYS = ('tag', 'usage')

    def __init__(self, tag, usage):
        self.tag = tag
        self.usage = usage

    @classmethod
    def from_dict(cls, d):
        for key in cls.REQUIRED_KEYS:
            if key not in d:
                raise ValueError('Missing keys for tag')

        return cls(*(d.get(k) for k in cls.REQUIRED_KEYS))

    def __eq__(self, other):
        """Test two tag objects for equality

        >>> Tag('u', 123) == Tag('u', 123)
        True
        >>> Tag('u', 123) == Tag('a', 345)
        False
        >>> Tag('u', 123) == 'x'
        False
        """
        if not isinstance(other, self.__class__):
            return False

        return all(getattr(self, k) == getattr(other, k) \
                for k in self.REQUIRED_KEYS)



class Episode(object):
    """Container Class for Episodes

    Attributes:
    title -
    url -
    podcast_title -
    podcast_url -
    description -
    website -
    released -
    mygpo_link -
    """

    REQUIRED_KEYS = ('title', 'url', 'podcast_title', 'podcast_url',
                     'description', 'website', 'released', 'mygpo_link')

    def __init__(self, title, url, podcast_title, podcast_url, description, website, released, mygpo_link):
        self.title = title
        self.url = url
        self.podcast_title = podcast_title
        self.podcast_url = podcast_url
        self.description = description
        self.website = website
        self.released = released
        self.mygpo_link = mygpo_link

    @classmethod
    def from_dict(cls, d):
        for key in cls.REQUIRED_KEYS:
            if key not in d:
                raise ValueError('Missing keys for episode')

        return cls(*(d.get(k) for k in cls.REQUIRED_KEYS))

    def __eq__(self, other):
        """Test two Episode objects for equality

        >>> Episode('a','b','c','d','e','f','g','h') == Episode('a','b','c','d','e','f','g','h')
        True
        >>> Episode('a','b','c','d','e','f','g','h') == Episode('s','t','u','v','w','x','y','z')
        False
        >>> Episode('a','b','c','d','e','f','g','h') == 'x'
        False
        """
        if not isinstance(other, self.__class__):
            return False

        return all(getattr(self, k) == getattr(other, k) \
            for k in self.REQUIRED_KEYS)

class PublicClient(object):
    """Client for the gpodder.net "anonymous" API

    This is the API client implementation that provides a
    pythonic interface to the parts of the gpodder.net
    Simple API that don't need user authentication.
    """
    FORMAT = 'json'

    def __init__(self, root_url=mygpoclient.ROOT_URL, client_class=json.JsonClient):
        """Creates a new Public API client

        The parameter root_url is optional and defaults to
        the main webservice. It can be either a hostname or
        a full URL (to force https, for instance).

        The parameter client_class is optional and should
        not need to be changed in normal use cases. If it
        is changed, it should provide the same interface
        as the json.JsonClient class in mygpoclient.
        """
        self._locator = locator.Locator(None, root_url)
        self._client = client_class(None, None)

    def get_toplist(self, count=mygpoclient.TOPLIST_DEFAULT):
        """Get a list of most-subscribed podcasts

        Returns a list of simple.Podcast objects.

        The parameter "count" is optional and describes
        the amount of podcasts that are returned. The
        default value is 50, the minimum value is 1 and
        the maximum value is 100.
        """
        uri = self._locator.toplist_uri(count, self.FORMAT)
        return [simple.Podcast.from_dict(x) for x in self._client.GET(uri)]

    def search_podcasts(self, query):
        """Search for podcasts on the webservice

        Returns a list of simple.Podcast objects.

        The parameter "query" specifies the search
        query as a string.
        """
        uri = self._locator.search_uri(query, self.FORMAT)
        return [simple.Podcast.from_dict(x) for x in self._client.GET(uri)]

    def get_podcasts_of_a_tag(self, tag, count=mygpoclient.TOPLIST_DEFAULT):
        """Get a list of most-subscribed podcasts of a Tag

        Returns a list of simple.Podcast objects.

        The parameter "tag" specifies the tag as a String

        The parameter "count" is optional and describes
        the amount of podcasts that are returned. The
        default value is 50, the minimum value is 1 and
        the maximum value is 100.
        """
        uri = self._locator.podcasts_of_a_tag_uri(tag, count)
        return [simple.Podcast.from_dict(x) for x in self._client.GET(uri)]

    def get_toptags(self, count=mygpoclient.TOPLIST_DEFAULT):
        """Get a list of most-used tags

        Returns a list of Tag objects.

        The parameter "count" is optional and describes
        the amount of podcasts that are returned. The
        default value is 50, the minimum value is 1 and
        the maximum value is 100.
        """
        uri = self._locator.toptags_uri(count)
        return [Tag.from_dict(x) for x in self._client.GET(uri)]

    def get_podcast_data(self, podcast_uri):
        """Get Metadata for the specified Podcast

        Returns a simple.Podcast object.

        The parameter "podcast_uri" specifies the URL of the Podcast.
        """
        uri = self._locator.podcast_data_uri(podcast_uri)
        return simple.Podcast.from_dict(self._client.GET(uri))

    def get_episode_data(self, podcast_uri, episode_uri):
        """Get Metadata for the specified Episode

        Returns a Episode object.

        The parameter "podcast_uri" specifies the URL of the Podcast,
        which this Episode belongs to

        The parameter "episode_uri" specifies the URL of the Episode
        """
        uri = self._locator.episode_data_uri(podcast_uri, episode_uri)
        return Episode.from_dict(self._client.GET(uri))
