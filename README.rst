python-media-hosts gets media info from sites like Youtube and Soundcloud.

**This library is broken and unmaintained, new contributors are welcome.**

Which informations does it return ?
==============================

Depending on the queried hosting service, the returned data can contain the
following keys:

- ``authors``
- ``beats_per_minute``
- ``comment_count``
- ``coverart_url``
- ``description``
- ``downloads``
- ``duration``
- ``favorite_count``
- ``genres``
- ``license``
- ``published``
- ``purchase_url``
- ``rating``
- ``recorded``
- ``tags``
- ``thumbnails``
- ``title``
- ``view_count``
- ``waveform_url``

The following keys are always present:

- ``id``
- ``service``
- ``type`` (audio or video)

Installation
============

	pip install media-hosts

media-hosts is compatible with python 2 and 3.

Dependencies:

- miss
- requests

Optional dependencies:

- python-dateutil: to parse dates returned by various APIs
- jsonpickle: for __main__.py

Usage
=====

From python::

	from media_hosts import MediaHosts, MediaHostException
	media_hosts = MediaHosts(_=_, settings=settings)
	media_hosts.get_info_by_url(url)

From the command line::

	$ python -m media_hosts 'https://www.youtube.com/watch?v=Gn3QXjNQNsk'

License
=======

`CC0 Public Domain Dedication <http://creativecommons.org/publicdomain/zero/1.0/>`_
