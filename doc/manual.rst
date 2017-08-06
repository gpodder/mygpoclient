Tutorial
========

This section gives a short how-to on how to use the library to interact with
the web service.

The Simple API client (``mygpoclient.simple.SimpleClient``)
-----------------------------------------------------------

The :class:`.SimpleClient` class is the most basic way of
interacting with the gpodder.net web service. You can use it to
provide quick integration of an existing application or in cases
where your client code has to be stateless.  Please use the
Advanced API client (which has a superset of :class:`.SimpleClient`'s
features) for more advanced use cases.

Importing the module
^^^^^^^^^^^^^^^^^^^^

Make sure that the :mod:`mygpoclient` package is in your ``sys.path``. You can
set the ``PYTHONPATH`` environment variable to the Git checkout folder or add
it to the ``sys.path`` list in Python. After that, you can import the
``simple`` module of the ``mygpoclient`` package:

.. code-block:: python

    from mygpoclient import simple


Creating a ``SimpleClient`` instance
------------------------------------

The client provides access to user-specific data, so you need to have the
username and password of the user you want to authenticate as ready. Also, as
gpodder.net is open source, and can potentially run on hosts different from
gpodder.net, you can optionally provide the hostname.

Let's suppose we want to authenticate as user ``john`` and the password
``secret`` to the default web service (that's '''gpodder.net'''). To create a
client object, we would use the following code:


.. code-block:: python

    client = simple.SimpleClient('john', 'secret')

If you have the web service running on another host (for example on port
``1337`` on the local host or ``localhost``), you can specify the
host and port as third argument to the :class:`.SimpleClient` constructor
(but you still need to provide username and password in this case):

.. code-block:: python

    client = simple.SimpleClient('john', 'secret', 'localhost:1337')


Downloading subscription lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can download a list of podcast subscriptions with
`SimpleClient.get_subscriptions(device_id)`. The given
`device_id` has to exist for the logged-in user. If the device does not
exist, a :class:`mygpoclient.http.NotFound` exception is raised.

To download the subscription list of the device ``legacy``, use:

.. code-block:: python

    subscriptions = client.get_subscriptions('legacy')


The resulting list contains URLs of all the subscribed podcasts for this device:

.. code-block:: python

    for url in subscriptions:
        print 'Subscribed to:', url


Uploading subscription lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with the download function, you can also upload subscriptions. For this, you
need to use the ``SimpleClient.put_subscriptions(device_id, urls)`` function.
The function returns ``True`` if the upload operation was successful, or False
otherwise. An example usage would be like this:

.. code-block:: python

    subscriptions = []
    subscriptions.append('http://example.org/episodes.rss')
    subscriptions.append('http://example.com/feeds/podcast.xml')
    client.put_subscriptions('gpodder-example-device', subscriptions)

The existing list of subscriptions is always overwritten, and the user's
subscription history will mark all podcasts that have been in the list before
but have been removed from the uploaded subscription list as unsubscribed.


Putting it all together (complete example)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have discussed the basics, we can write a simple but
feature-complete command-line application for downloading and uploading
subscription lists (this code can also be found in the source tree as `simple-client <https://github.com/gpodder/mygpoclient/blob/master/bin/mygpo-simple-client>`_:

.. literalinclude:: ../bin/mygpo-simple-client
    :language: python
    :linenos:


The Advanced API client (``mygpoclient.api.MygPodderClient``)
-------------------------------------------------------------

The :class:`.MygPodderClient` class inherits from :class:`.SimpleClient`, so
you can use both the Simple API and Advanced API functionality with this class.


Working with subscription lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given a device ID, you can update the list of subscriptions via the
:meth:`.update_subscriptions` method. You need to pass a device_id and
two lists (one for the URLs that have been added and one for the URLs that have
been removed) to update the subscriptions on the server, for example:

.. code-block:: python

    from mygpoclient import api

    client = api.MygPodderClient('myusername', 'S3cr3tPassw0rd')

    to_add = ['http://lugradio.org/episodes.rss']
    to_remove = ['http://example.org/episodes.rss',
                 'http://example.com/feed.xml']
    result = client.update_subscriptions('abcdevice', to_add, to_remove)

You can use empty lists if you just add or remove items. As you can see in the
code example, the function (if successful) returns a UpdateResult object. The
UpdateResult object contains a `update_urls` attribute that is a list of
`(old_url, new_url)` tuples in case the server has re-written URLs. According
to the API documentation, the client application must update the old_url values
with new_url values (these have been sanitized). The `since` attribute of the
result object can be used for requesting changes since the last upload, like
this:


.. code-block:: python

    updates = client.pull_subscriptions('abcdevice', result.since)

The `updates` return value here is a :class:`.SubscriptionChanges` object that
contains a new ``since`` attribute (that can be used for subsequent requests)
and two lists (``add`` and ``remove``) of URLs that should be processed by the
client by creating and removing subscriptions.


Synchronizing episode actions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

''TODO''


Enumerating and modifying devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :class:`.MygPodderClient` class provides two methods for dealing with devices:
:meth:`.get_devices` (which returns a list of :class:`PodcastDevice` objects) and
:meth:`.update_device_settings` for modifying the device-specific
settings on the server side. Here is an example script to use both
functions to rename all users's device to "My Device" on the server:


.. code-block:: python

    client = api.MygPodderClient('john', '53cr3t')

    for device in client.get_devices():
        print 'Changing name of', device.device_id
        client.update_device_settings(device.device_id, caption='My Device')


The Public API client (``mygpoclient.public.PublicClient``)
-----------------------------------------------------------

This client does not need authentication and can be used to query and retrieve
public data from the web service.


Toplist retrieval
^^^^^^^^^^^^^^^^^

You can use the :meth:`.get_toplist` method on a :class:`.PublicClient`
instance to retrieve a list of podcast toplist entries:


.. code-block:: python

    from mygpoclient import public

    client = public.PublicClient()

    toplist = client.get_toplist()
    for index, entry in enumerate(toplist):
        print '%4d. %s (%d)' % (index+1, entry.title, entry.subscribers)


Searching for podcasts
^^^^^^^^^^^^^^^^^^^^^^

Searching is done using :meth:`.search_podcasts` method of
:class:`.PublicClient` like this:


.. code-block:: python

    from mygpoclient import public

    client = public.PublicClient()

    search_results = client.search_podcasts('outlaws')
    for result in search_results:
        print result.title
        print result.url
        print '-'*50

