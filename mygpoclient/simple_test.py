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

from mygpoclient import simple
from mygpoclient import testing

import unittest

class Test_Podcast(unittest.TestCase):
    def test_podcastFromDict_raisesValueError_missingKey(self):
        self.assertRaises(ValueError,
                simple.Podcast.from_dict, {'url': 'a', 'title': 'b'})

class Test_SimpleClient(unittest.TestCase):
    USERNAME = 'a'
    PASSWORD = 'b'
    DEVICE_NAME = 'x'
    SUBSCRIPTIONS = [
            'http://lugradio.org/episodes.rss',
            'http://feeds2.feedburner.com/LinuxOutlaws',
    ]
    SUBSCRIPTIONS_JSON = b"""
      ["http://lugradio.org/episodes.rss",
       "http://feeds2.feedburner.com/LinuxOutlaws"]
    """
    SUGGESTIONS = [
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
    SUGGESTIONS_JSON = b"""
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

    def setUp(self):
        self.fake_client = testing.FakeJsonClient()
        self.client = simple.SimpleClient(self.USERNAME, self.PASSWORD,
                client_class=self.fake_client)

    def test_putSubscriptions(self):
        self.fake_client.response_value = b''
        result = self.client.put_subscriptions(self.DEVICE_NAME, self.SUBSCRIPTIONS)
        self.assertEquals(result, True)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_getSubscriptions(self):
        self.fake_client.response_value = self.SUBSCRIPTIONS_JSON
        subscriptions = self.client.get_subscriptions(self.DEVICE_NAME)
        self.assertEquals(subscriptions, self.SUBSCRIPTIONS)
        self.assertEquals(len(self.fake_client.requests), 1)

    def test_getSuggestions(self):
        self.fake_client.response_value = self.SUGGESTIONS_JSON
        suggestions = self.client.get_suggestions(50)
        self.assertEquals(suggestions, self.SUGGESTIONS)
        self.assertEquals(len(self.fake_client.requests), 1)


class Test_MissingCredentials(unittest.TestCase):
    DEVICE_NAME = 'unit-test-device'

    def test_getSubscriptions_UserAndPassAreNone(self):
        client = simple.SimpleClient(None, None, client_class=testing.FakeJsonClient())
        self.assertRaises(simple.MissingCredentials, client.get_subscriptions, (self.DEVICE_NAME,))

    def test_getSubscriptions_EmptyUserAndPass(self):
        client = simple.SimpleClient('', '', client_class=testing.FakeJsonClient())
        self.assertRaises(simple.MissingCredentials, client.get_subscriptions, (self.DEVICE_NAME,))

    def test_getSubscriptions_EmptyPassword(self):
        client = simple.SimpleClient('user', '', client_class=testing.FakeJsonClient())
        self.assertRaises(simple.MissingCredentials, client.get_subscriptions, (self.DEVICE_NAME,))

    def test_getSubscriptions_EmptyUsername(self):
        client = simple.SimpleClient('', 'pass', client_class=testing.FakeJsonClient())
        self.assertRaises(simple.MissingCredentials, client.get_subscriptions, (self.DEVICE_NAME,))

