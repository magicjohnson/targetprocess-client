
TargetProcess Client

Python library to help getting data from `TargetProcess API <http://dev.targetprocess.com/rest/getting_started>`_

.. image:: https://img.shields.io/pypi/v/targetprocess-client.svg
    :target: https://badge.fury.io/py/targetprocess-client
    :alt: Pypi

.. image:: https://travis-ci.org/magicjohnson/targetprocess-client.svg?branch=master
    :target: https://travis-ci.org/magicjohnson/targetprocess-client
    :alt: Travis CI

.. image:: https://codecov.io/github/magicjohnson/targetprocess-client/coverage.svg?branch=master
    :target: https://codecov.io/github/magicjohnson/targetprocess-client?branch=master
    :alt: Codecov

.. image:: https://www.quantifiedcode.com/api/v1/project/8cdc9e5652dd4aaf8c8465b788966ea3/badge.svg
    :target: https://www.quantifiedcode.com/app/project/8cdc9e5652dd4aaf8c8465b788966ea3
    :alt: Code issues

================
Getting the code
================

The code is hosted at https://github.com/magicjohnson/targetprocess-client

Check out the latest development version with::

    $ git clone git://github.com/magicjohnson/targetprocess-client.git

==========
Installing
==========

You can install targetprocess-client using::

    $ pip install targetprocess-client

or get the code and run install::

    $ cd targetprocess-client
    $ python setup.py install

==============
Usage examples
==============

Create client instance:

.. code-block:: python

    from targetprocess.api import TargetProcessAPIClient
    from targetprocess.serializers import TargetProcessSerializer
    tp = TargetProcessAPIClient(api_url='https://md5.tpondemand.com/api/v1/', user='user', password='pass')

Get collection of UserStories:

.. code-block:: python

    stories_json = tp.get_stories(take=5, include="[Id,Name,CreateDate]")
    stories = TargetProcessSerializer.deserialize(stories_json)

Get UserStory item

.. code-block:: python

    story_json = tp.get_story(360, include="[Id,Name,CreateDate]")
    story = TargetProcessSerializer.deserialize(story_json)

Update item

.. code-block:: python

    data = {'Name': 'New name'}
    tp.update_story(360, data)

Request "unregistered" collection (that client doesn't have predefined methods for)

.. code-block:: python

    tp.get_collection(collection="Epics", take=2)
    tp.get_resource(collection="Epics", entity_id=427)
    tp.update_resource(collection="Epics", entity_id=427, data={'Name': 'New Epic name'})
