Muffin-APIClient
#################

.. _description:

**Muffin-APIClient** -- Its a plugin for Muffin_ framework which provides support
for external APIs

.. _badges:

.. image:: https://github.com/klen/muffin-apiclient/workflows/tests/badge.svg
    :target: https://github.com/klen/muffin-apiclient/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/muffin-apiclient
    :target: https://pypi.org/project/muffin-apiclient/
    :alt: PYPI Version

.. image:: https://img.shields.io/pypi/pyversions/muffin-apiclient
    :target: https://pypi.org/project/muffin-apiclient/
    :alt: Python Versions

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.9

.. _installation:

Installation
=============

**Muffin-APIClient** should be installed using pip: ::

    pip install muffin-apiclient

.. _usage:

Usage
=====


Initialize and setup the plugin:

.. code-block:: python

    import muffin
    import muffin_apiclient

    # Create Muffin Application
    app = muffin.Application('example')

    # Initialize the plugin
    # As alternative: apiclient = muffin_apiclient.Plugin(app, **options)
    apiclient = muffin_apiclient.Plugin()
    apiclient.setup(app, root_url='https://api.github.com')

Github API (https://developer.github.com/v4/):

.. code:: python

    github = muffin_apiclient.Plugin(app, name='github', root_url='https://api.github.com', defaults={
        'headers': {
            'Authorization': 'token OAUTH-TOKEN'
        }
    })

    # Read information about the current repository
    repo = await github.api.repos.klen['muffin-apiclient'].get()
    print(repo)  # dict parsed from Github Response JSON


Slack API (https://api.slack.com/web):

.. code:: python

    slack = muffin_apiclient.Plugin(app, name='slack', root_url='https://slack.com/api', defaults={
        'headers': {
            'Authorization': 'token OAUTH-TOKEN'
        }
    })

    # Update current user status (we don't care about this response)
    await client.api['users.profile.set'].post(json={
        'profile': {
            'status_text': 'working',
            'status_emoji': ':computer:'
            'status_expiration': 30,
        }
    }, read_response_body=False)


And etc

Options
-------

=========================== =========================== ===========================
Name                        Default value               Desctiption
--------------------------- --------------------------- ---------------------------
**root_url**                ``None``                    Define general root URL for the client
**timeout**                 ``None``                    Define client timeout
**backend_type**            ``httpx``                   APIClient backend (httpx|aiohttp)
**backend_options**         ``{}``                      Backend options
**raise_for_status**        ``True``                    Raise errors for HTTP statuses (300+)
**read_response_body**      ``True``                    Read responses
**parse_response_body**     ``True``                    Parse responses (load json, etc)
**client_defaults**         ``{}``                      Default client values (headers, auth, etc)
=========================== =========================== ===========================


You are able to provide the options when you are initiliazing the plugin:

.. code-block:: python

    apiclient.setup(app, root_url='https://api.github.com')


Or setup it inside ``Muffin.Application`` config using the ``APICLIENT_`` prefix:

.. code-block:: python

   APICLIENT_ROOT_URL = 'https://api.github.com'

``Muffin.Application`` configuration options are case insensitive





.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/muffin-apiclient/issues

.. _contributing:

Contributing
============

Development of Muffin-APIClient happens at: https://github.com/klen/muffin-apiclient


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
========

Licensed under a `MIT license`_.

.. _links:


.. _klen: https://github.com/klen
.. _Muffin: https://github.com/klen/muffin

.. _MIT license: http://opensource.org/licenses/MIT
