# -*- coding: utf-8 -*-
# mygpo-feedservice Client
# Copyright (C) 2011 Stefan Kögl
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

from __future__ import absolute_import

import time

try:
    # Python 3
    from urllib.parse import urljoin, urlencode

except ImportError:
    # Python 2
    from urlparse import urljoin
    from urllib import urlencode

from datetime import datetime
from email import utils

import mygpoclient.json

try:
    # Prefer the usage of the simplejson module, as it
    # is most likely newer if it's installed as module
    # than the built-in json module (and is mandatory
    # in Python versions before 2.6, anyway).
    import simplejson as json
except ImportError:
    # Python 2.6 ships the "json" module by default
    import json


BASE_URL='http://mygpo-feedservice.appspot.com'


class FeedServiceResponse(list):
    """
    Encapsulates the relevant data of a mygpo-feedservice response
    """

    def __init__(self, feeds, last_modified, feed_urls):
        super(FeedServiceResponse, self).__init__(feeds)
        self.last_modified = last_modified
        self.feed_urls = feed_urls
        self.indexed_feeds = {}
        for feed in feeds:
            for url in feed['urls']:
                self.indexed_feeds[url] = feed


    def get_feeds(self):
        """
        Returns the parsed feeds in order of the initial request
        """
        return (self.get_feed(url) for url in self.feed_urls)


    def get_feed(self, url):
        """
        Returns the parsed feed for the given URL
        """
        return self.indexed_feeds.get(url, None)


class FeedserviceClient(mygpoclient.json.JsonClient):
    """A special-cased JsonClient for mygpo-feedservice"""

    def __init__(self, username=None, password=None, base_url=BASE_URL):
        self._base_url = base_url
        super(FeedserviceClient, self).__init__(username, password)

    def _prepare_request(self, method, uri, data):
        """Sets headers required by mygpo-feedservice

        Expects a dict with keys feed_urls and (optionally) last_modified"""

        # send URLs as POST data to avoid any length
        # restrictions for the query parameters
        post_data = [('url', feed_url) for feed_url in data['feed_urls']]
        post_data = urlencode(post_data)

        # call _prepare_request directly from HttpClient, because
        # JsonClient would JSON-encode our POST-data
        request = mygpoclient.http.HttpClient._prepare_request(method, uri, post_data)
        request.add_header('Accept', 'application/json')
        request.add_header('Accept-Encoding', 'gzip')

        last_modified = data.get('last_modified', None)
        if last_modified is not None:
            request.add_header('If-Modified-Since', self.format_header_date(last_modified))

        return request


    def _process_response(self, response):
        """ Extract Last-modified header and passes response body
            to JsonClient for decoding"""

        last_modified = self.parse_header_date(response.headers['last-modified'])
        feeds = super(FeedserviceClient, self)._process_response(response)
        return feeds, last_modified


    def parse_feeds(self, feed_urls, last_modified=None, strip_html=False,
                use_cache=True, inline_logo=False, scale_logo=None,
                logo_format=None):
        """
        Passes the given feed-urls to mygpo-feedservice to be parsed
        and returns the response
        """

        url = self.build_url(strip_html=strip_html, use_cache=use_cache,
                inline_logo=inline_logo, scale_logo=scale_logo,
                logo_format=logo_format)

        request_data = dict(feed_urls=feed_urls, last_modified=last_modified)

        feeds, last_modified = self.POST(url, request_data)

        return FeedServiceResponse(feeds, last_modified, feed_urls)


    def build_url(self, **kwargs):
        """
        Parameter such as strip_html, scale_logo, etc are pased as kwargs
        """

        query_url = urljoin(self._base_url, 'parse')

        args = list(kwargs.items())
        args = [k_v for k_v in args if k_v[1] is not None]

        # boolean flags are represented as 1 and 0 in the query-string
        args = [(k_v1[0], int(k_v1[1]) if isinstance(k_v1[1], bool) else k_v1[1]) for k_v1 in args]
        args = urlencode(dict(args))

        url = '%s?%s' % (query_url, args)
        return url


    @staticmethod
    def parse_header_date(date_str):
        """
        Parses dates in RFC2822 format to datetime objects
        """
        if not date_str:
            return None
        ts = time.mktime(utils.parsedate(date_str))
        return datetime.utcfromtimestamp(ts)

    @staticmethod
    def format_header_date(datetime_obj):
        """
        Formats the given datetime object for use in HTTP headers
        """
        return utils.formatdate(time.mktime(datetime_obj.timetuple()))
