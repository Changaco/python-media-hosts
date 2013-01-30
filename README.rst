python-media-hosts gets media info from sites like Youtube and Soundcloud.

Installation
============

	pip install media-hosts

media-hosts is compatible with python 2 and 3.

Dependencies:

- miss

Optional dependencies:

- python-dateutil: to parse dates returned by various APIs
- gdata: for some Youtube data
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

LGPLv3+
