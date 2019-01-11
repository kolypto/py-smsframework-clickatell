`Build
Status <https://travis-ci.org/kolypto/py-smsframework-clickatell>`__
`Pythons <.travis.yml>`__

SMSframework Clickatell Provider
================================

`Clickatell <https://www.clickatell.com/>`__ Provider for
`smsframework <https://pypi.python.org/pypi/smsframework/>`__.

You need a “Developers’ Central” Clickatell account with an HTTP API set
up. From the API, you need: api_id, username, password.

Installation
============

Install from pypi:

::

   $ pip install smsframework_clickatell

To receive SMS messages, you need to ensure that `Flask
microframework <http://flask.pocoo.org>`__ is also installed:

::

   $ pip install smsframework_clickatell[receiver]

Initialization
==============

.. code:: python

   from smsframework import Gateway
   from smsframework_clickatell import ClickatellProvider

   gateway = Gateway()
   gateway.add_provider('clickatell', ClickatellProvider,
       api_id=1,
       user='kolypto',
       password='123',
       https=False
   )

Config
------

Source: /smsframework_clickatell/provider.py

-  ``api_id: str``: API ID to use
-  ``user: str``: Account username
-  ``password: str``: Account password
-  ``https: bool``: Use HTTPS for outgoing messages? Default: ``False``

Sending Parameters
==================

Provider-specific sending params:

-  ``deliv_time: int``: Delay the delivery for X minutes

Example:

.. code:: python

   from smsframework import OutgoingMessage

   gateway.send(OutgoingMessage('+123', 'hi').params(deliv_time=15))

Additional Information
======================

OutgoingMessage.meta
--------------------

None.

IncomingMessage.meta
--------------------

-  ``api_id: str``: API id
-  ``charset: str``: Message character set (when applicable, else -
   None)
-  ``udh: str``: Header Data (when applicable, else - None)

MessageStatus.meta
------------------

-  ``status: int``: Message status code
-  ``api_id: str``: API id
-  ``charge: float``: Charged funds

Public API
==========

ClickatellProvider.get_balance()
--------------------------------

Returns the credist left on the account:

.. code:: python

   provider = gateway.get_provider('clickatell')
   provider.get_balance() #-> 10.6

Receivers
=========

Source: /smsframework_clickatell/receiver.py

Message Receiver: /im
---------------------

After a number is purchased, go to Receive Messages > Manage long
numbers / short codes, and then click the ‘Edit’ link of the two-way
number which you would like to configure. Set “Reply Path” to “HTTP Get”
\| “HTTP Post”, in the field - put the message receiver URL.

-  “Username & Password” is not supported
-  “Secondary callback” is up to you

Message Receiver URL: ``<provider-name>/im``

Status Receiver: /status
------------------------

To start getting status reports from Clickatell, edit the HTTP API in
the admin panel and click on “Enable your app to receive message
delivery notifications”. In the field, put the receiver URL.

-  Status receiver only supports “HTTP Get” and “HTTP Post” methods.
-  “basic HTTP Authentication” is not supported

Status Receiver URL: ``<provider-name>/status``
