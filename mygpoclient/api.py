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

from mygpoclient import simple

# Additional error types for the advanced API client
class InvalidResponse(Exception): pass


class SubscriptionChanges(object):
    """Container for subscription changes

    Attributes:
        add - A list of URLs that have been added
        remove - A list of URLs that have been removed
        since - A timestamp value for use in future requests
    """
    def __init__(self, add, remove, since):
        self.add = add
        self.remove = remove
        self.since = since

class EpisodeActionChanges(object):
    """Container for added episode actions

    Attributes:
        actions - A list of EpisodeAction objects
        since - A timestamp value for use in future requests
    """
    def __init__(self, actions, since):
        self.actions = actions
        self.since = since

class PodcastDevice(object):
    """This class encapsulates a podcast device

    Attributes:
        device_id - The ID used to refer to this device
        caption - A user-defined "name" for this device
        type - A valid type of podcast device (see VALID_TYPES)
        subscriptions - The number of podcasts this device is subscribed to
    """
    VALID_TYPES = ('desktop', 'laptop', 'mobile', 'server', 'other')

    def __init__(self, device_id, caption, type, subscriptions):
        # Check if the device type is valid
        if type not in self.VALID_TYPES:
            raise ValueError('Invalid device type (see VALID_TYPES)')

        # Check if subsciptions is a numeric value
        try:
            int(subscriptions)
        except:
            raise ValueError('Subscription must be a numeric value')

        self.device_id = device_id
        self.caption = caption
        self.type = type
        self.subscriptions = int(subscriptions)

class EpisodeAction(object):
    """This class encapsulates an episode action

    The mandatory attributes are:
        podcast - The feed URL of the podcast
        episode - The enclosure URL or GUID of the episode
        action - One of 'download', 'play', 'delete' or 'new'

    The optional attributes are:
        device - The device_id on which the action has taken place
        timestamp - When the action took place (in XML time format)
        position - The current play position in HH:MM:SS format

    The attribute "position" is only valid for "play" action types.
    """
    VALID_ACTIONS = ('download', 'play', 'delete', 'new')

    def __init__(self, podcast, episode, action,
            device=None, timestamp=None, position=None):
        # Check if the action is valid
        if action not in self.VALID_ACTIONS:
            raise ValueError('Invalid action type (see VALID_TYPES)')

        # Do not allow position changes on non-play actions
        if action != 'play' and position is not None:
            raise ValueError('Position can only be set for the "play" action')

        # Check the format of the timestamp value
        if timestamp is not None:
            pass # FIXME: Check for valid XML timestamp

        # Check the format of the position value
        if position is not None:
            pass # FIXME: Check for valid HH:MM:SS timestamp

        self.podcast = podcast
        self.episode = episode
        self.action = action
        self.device = device
        self.timestamp = timestamp
        self.position = position

    def to_dictionary(self):
        d = {}

        for mandatory in ('podcast', 'episode', 'action'):
            value = getattr(self, mandatory)
            d[mandatory] = value

        for optional in ('device', 'timestamp', 'position'):
            value = getattr(self, optional)
            if value is not None:
                d[optional] = value

        return d


class MygPodderClient(simple.SimpleClient):
    """my.gpodder.org API Client

    This is the API client that implements both the Simple and
    Advanced API of my.gpodder.org. See the SimpleClient class
    for a smaller class that only implements the Simple API.
    """
    def update_subscriptions(self, device_id, add_urls=[], remove_urls=[]):
        """Update the subscription list for a given device.

        Returns the timestamp that can be used for retrieving changes.
        """
        uri = self._locator.add_remove_subscriptions_uri(device_id)
        return 0

    def pull_subscriptions(self, device_id, since=None):
        """Downloads subscriptions since the time of the last update

        The "since" parameter should be a timestamp that has been
        retrieved previously by a call to update_subscriptions or
        pull_subscriptions.

        Returns a SubscriptionChanges object with two lists (one for
        added and one for removed podcast URLs) and a "since" value
        that can be used for future calls to this method.
        """
        uri = self._locator.subscription_updates_uri(device_id, since)
        return SubscriptionChanges([], [], 0)

    def upload_episode_actions(self, actions=[]):
        """Uploads a list of EpisodeAction objects to the server

        Returns the timestamp that can be used for retrieving changes.
        """
        uri = self._locator.upload_episode_actions_uri()
        return 0

    def download_episode_actions(self, since=None,
            podcast=None, device_id=None):
        """Downloads a list of EpisodeAction objects from the server

        Returns a EpisodeActionChanges object with the list of
        new actions and a "since" timestamp that can be used for
        future calls to this method when retrieving episodes.
        """
        uri = self._locator.download_episode_actions_uri(since,
                podcast, device_id)
        return EpisodeActionChanges([], 0)

    def update_device_settings(self, device_id, caption=None, type=None):
        """Update the description of a device on the server

        This changes the caption and/or type of a given device
        on the server. If the device does not exist, it is
        created with the given settings.

        The parameters caption and type are both optional and
        when set to a value other than None will be used to
        update the device settings.

        Returns True if the request succeeded, False otherwise.
        """
        uri = self._locator.device_settings_uri(device_id)
        return False

    def get_devices(self):
        """Returns a list of this user's PodcastDevice objects

        The resulting list can be used to display a selection
        list to the user or to determine device IDs to pull
        the subscription list from.
        """
        return []



