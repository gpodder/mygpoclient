# -*- coding: utf-8 -*-
# gpodder.net API Client
# Copyright (C) 2009-2011 Thomas Perl and the gPodder Team
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

from mygpoclient import public
from mygpoclient import simple
from mygpoclient import testing

import unittest

class Test_PublicClient(unittest.TestCase):
    TOPLIST_JSON = """
    [{
    "website": "http://linuxoutlaws.com/podcast", 
    "description": "Open source talk with a serious attitude", 
    "title": "Linux Outlaws", 
    "url": "http://feeds.feedburner.com/linuxoutlaws", 
    "subscribers_last_week": 1736, 
    "subscribers": 1736, 
    "mygpo_link": "http://www.gpodder.net/podcast/11092", 
    "logo_url": "http://linuxoutlaws.com/files/albumart-itunes.jpg"
    }, 
    {
    "website": "http://syndication.mediafly.com/redirect/show/d581e9b773784df7a56f37e1138c037c", 
    "description": "We are not talking dentistry here; FLOSS all about Free Libre Open Source Software. Join hosts Randal Schwartz and Leo Laporte every Saturday as they talk with the most interesting and important people in the Open Source and Free Software community.", 
    "title": "FLOSS Weekly Video (large)", 
    "url": "http://feeds.twit.tv/floss_video_large",
    "subscribers_last_week": 50, 
    "subscribers": 50, 
    "mygpo_link": "http://www.gpodder.net/podcast/31991", 
    "logo_url": "http://static.mediafly.com/publisher/images/06cecab60c784f9d9866f5dcb73227c3/icon-150x150.png"
    }]
    """
    TOPLIST = [
            simple.Podcast('http://feeds.feedburner.com/linuxoutlaws',
                'Linux Outlaws',
                'Open source talk with a serious attitude',
                'http://linuxoutlaws.com/podcast',
                1736, 1736,
                'http://www.gpodder.net/podcast/11092',
                'http://linuxoutlaws.com/files/albumart-itunes.jpg'),
            simple.Podcast('http://feeds.twit.tv/floss_video_large',
                'FLOSS Weekly Video (large)',
                'We are not talking dentistry here; FLOSS all about Free Libre Open Source Software. Join hosts Randal Schwartz and Leo Laporte every Saturday as they talk with the most interesting and important people in the Open Source and Free Software community.',
                'http://syndication.mediafly.com/redirect/show/d581e9b773784df7a56f37e1138c037c',
                50, 50,
                'http://www.gpodder.net/podcast/31991',
                'http://static.mediafly.com/publisher/images/06cecab60c784f9d9866f5dcb73227c3/icon-150x150.png'),
    ]
    SEARCHRESULT_JSON = """
    [{
    "website": "http://linuxoutlaws.com/podcast", 
    "description": "Open source talk with a serious attitude", 
    "title": "Linux Outlaws", 
    "url": "http://feeds.feedburner.com/linuxoutlaws", 
    "subscribers_last_week": 1736, 
    "subscribers": 1736, 
    "mygpo_link": "http://www.gpodder.net/podcast/11092", 
    "logo_url": "http://linuxoutlaws.com/files/albumart-itunes.jpg"
    }, 
    {
    "website": "http://syndication.mediafly.com/redirect/show/d581e9b773784df7a56f37e1138c037c", 
    "description": "We are not talking dentistry here; FLOSS all about Free Libre Open Source Software. Join hosts Randal Schwartz and Leo Laporte every Saturday as they talk with the most interesting and important people in the Open Source and Free Software community.", 
    "title": "FLOSS Weekly Video (large)", 
    "url": "http://feeds.twit.tv/floss_video_large",
    "subscribers_last_week": 50, 
    "subscribers": 50, 
    "mygpo_link": "http://www.gpodder.net/podcast/31991", 
    "logo_url": "http://static.mediafly.com/publisher/images/06cecab60c784f9d9866f5dcb73227c3/icon-150x150.png"
    }]
    """
    SEARCHRESULT = [
            simple.Podcast('http://feeds.feedburner.com/linuxoutlaws',
                'Linux Outlaws',
                'Open source talk with a serious attitude',
                'http://linuxoutlaws.com/podcast',
                1736, 1736,
                'http://www.gpodder.net/podcast/11092',
                'http://linuxoutlaws.com/files/albumart-itunes.jpg'),
            simple.Podcast('http://feeds.twit.tv/floss_video_large',
                'FLOSS Weekly Video (large)',
                'We are not talking dentistry here; FLOSS all about Free Libre Open Source Software. Join hosts Randal Schwartz and Leo Laporte every Saturday as they talk with the most interesting and important people in the Open Source and Free Software community.',
                'http://syndication.mediafly.com/redirect/show/d581e9b773784df7a56f37e1138c037c',
                50, 50,
                'http://www.gpodder.net/podcast/31991',
                'http://static.mediafly.com/publisher/images/06cecab60c784f9d9866f5dcb73227c3/icon-150x150.png'),
    ]

    def setUp(self):
        self.fake_client = testing.FakeJsonClient()
        self.client = public.PublicClient(client_class=self.fake_client)

    def test_getToplist(self):
        self.fake_client.response_value = self.TOPLIST_JSON
        result = self.client.get_toplist()
        self.assertEquals(result, self.TOPLIST)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_searchPodcasts(self):
        self.fake_client.response_value = self.SEARCHRESULT_JSON
        result = self.client.search_podcasts('wicked')
        self.assertEquals(result, self.SEARCHRESULT)
        self.assertEquals(len(self.fake_client.requests), 1)

