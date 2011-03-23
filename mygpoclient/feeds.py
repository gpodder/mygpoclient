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

import urllib, urllib2, urlparse, time
from datetime import datetime
from email import utils
import mygpoclient

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



def parse_feeds(feed_urls, last_modified=None, strip_html=None, use_cache=None,
                inline_logo=None, scale_logo=None, logo_format=None):
    """
    Passes the given feed-urls to mygpo-feedservice to be parsed
    and returns the response
    """

    url = build_url(strip_html=strip_html, use_cache=use_cache,
                inline_logo=inline_logo, scale_logo=scale_logo,
                logo_format=logo_format)

    resp = send_request(feed_urls, url, last_modified)

    last_modified = parse_header_date(resp.headers['last-modified'])

    feeds = json.loads(resp.read())

    return FeedServiceResponse(feeds, last_modified, feed_urls)


def build_url(**kwargs):
    """
    Parameter such as strip_html, scale_logo, etc are pased as kwargs
    """

    query_url = urlparse.urljoin(BASE_URL, 'parse')

    args = kwargs.items()
    args = filter(lambda (k, v): v is not None, args)

    # boolean flags are represented as 1 and 0 in the query-string
    args = map(lambda (k, v): (k, int(v) if isinstance(v, bool) else v), args)
    args = ['%s=%s' % i for i in args]

    url = '%s?%s' % (query_url, '&'.join(args))
    return url


def send_request(feed_urls, url, last_modified=None):
    """
    Adds all required headers, sends the request and returns the response
    """

    req = urllib2.Request(url)
    req.add_header('User-Agent', mygpoclient.user_agent)
    req.add_header('Accept', 'application/json')
    req.add_header('Accept-Encoding', 'gzip')

    if last_modified is not None:
        req.add_header('If-Modified-Since', format_header_date(last_modified))

    post_data = [('url', feed_url) for feed_url in feed_urls]
    data = urllib.urlencode(post_data)
    req.add_data(data)

    return urllib2.urlopen(req)


def parse_header_date(date_str):
    """
    Parses dates in RFC2822 format to datetime objects
    """
    if not date_str:
        return None
    ts = time.mktime(utils.parsedate(date_str))
    return datetime.utcfromtimestamp(ts)

def format_header_date(datetime_obj):
    """
    Formats the given datetime object for use in HTTP headers
    """
    return utils.formatdate(time.mktime(datetime_obj.timetuple()))
