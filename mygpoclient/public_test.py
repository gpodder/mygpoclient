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

from mygpoclient import public
from mygpoclient import simple
from mygpoclient import testing

import unittest

class Test_Tag(unittest.TestCase):
    def test_tagFromDict_raisesValueError_missingKey(self):
        self.assertRaises(ValueError,public.Tag.from_dict, {'tag':'abcde'} )

class Test_Episode(unittest.TestCase):
    def test_episodeFromDict_raisesValueError_missingKey(self):
        self.assertRaises(ValueError,public.Episode.from_dict, {'title':'foobar','podcast_url':'http://www.podcast.com'})

class Test_PublicClient(unittest.TestCase):
    TOPLIST_JSON = b"""
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
    SEARCHRESULT_JSON = b"""
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

    TOPTAGS_JSON = b"""
    [
        {"tag": "Technology",
         "usage": 530 },
        {"tag": "Arts",
         "usage": 400}
    ]
    """
    TOPTAGS = [
               public.Tag('Technology',530),
               public.Tag('Arts',400)
    ]

    PODCAST_JSON = b"""
    {
    "website": "http://linuxoutlaws.com/podcast",
    "description": "Open source talk with a serious attitude",
    "title": "Linux Outlaws",
    "url": "http://feeds.feedburner.com/linuxoutlaws",
    "subscribers_last_week": 1736,
    "subscribers": 1736,
    "mygpo_link": "http://www.gpodder.net/podcast/11092",
    "logo_url": "http://linuxoutlaws.com/files/albumart-itunes.jpg"
    }
    """
    PODCAST = simple.Podcast('http://feeds.feedburner.com/linuxoutlaws',
                'Linux Outlaws',
                'Open source talk with a serious attitude',
                'http://linuxoutlaws.com/podcast',
                1736, 1736,
                'http://www.gpodder.net/podcast/11092',
                'http://linuxoutlaws.com/files/albumart-itunes.jpg')

    EPISODE_JSON = b"""
    {"title": "TWiT 245: No Hitler For You",
    "url": "http://www.podtrac.com/pts/redirect.mp3/aolradio.podcast.aol.com/twit/twit0245.mp3",
    "podcast_title": "this WEEK in TECH - MP3 Edition",
    "podcast_url": "http://leo.am/podcasts/twit",
    "description": "[...]",
    "website": "http://www.podtrac.com/pts/redirect.mp3/aolradio.podcast.aol.com/twit/twit0245.mp3",
    "released": "2010-12-25T00:30:00",
    "mygpo_link": "http://gpodder.net/episode/1046492"}
    """
    EPISODE = public.Episode('TWiT 245: No Hitler For You',
                             'http://www.podtrac.com/pts/redirect.mp3/aolradio.podcast.aol.com/twit/twit0245.mp3',
                             'this WEEK in TECH - MP3 Edition',
                             'http://leo.am/podcasts/twit',
                             '[...]',
                             'http://www.podtrac.com/pts/redirect.mp3/aolradio.podcast.aol.com/twit/twit0245.mp3',
                             '2010-12-25T00:30:00',
                             'http://gpodder.net/episode/1046492'
                             )

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

    def test_getPodcastsOfATag(self):
        self.fake_client.response_value = self.SEARCHRESULT_JSON
        result = self.client.get_podcasts_of_a_tag('wicked')
        self.assertEquals(result, self.SEARCHRESULT)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_getTopTags(self):
        self.fake_client.response_value = self.TOPTAGS_JSON
        result = self.client.get_toptags()
        self.assertEquals(result, self.TOPTAGS)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_getPodcastData(self):
        self.fake_client.response_value = self.PODCAST_JSON
        result = self.client.get_podcast_data('http://feeds.feedburner.com/linuxoutlaws')
        self.assertEquals(result, self.PODCAST)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_getEpisodeData(self):
        self.fake_client.response_value = self.EPISODE_JSON
        result = self.client.get_episode_data('http://leo.am/podcasts/twit','http://www.podtrac.com/pts/redirect.mp3/aolradio.podcast.aol.com/twit/twit0245.mp3')
        self.assertEquals(result, self.EPISODE)
        self.assertEquals(len(self.fake_client.requests), 1)
