# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import math
import binascii

from .const import Features


class ClickatellApiError(RuntimeError):
    def __init__(self, code, message):
        self.code = code
        super(ClickatellApiError, self).__init__(message)


class ClickatellHttpApi(object):
    """ Clickatell HTTP API client """

    def __init__(self, api_id, user, password, https=False):
        """ Create an authenticated client

            :param api_id: Authentication: API ID
            :param user: Authentication: username
            :param password: Authentication: password
            :type https: bool
            :param https: Use HTTPS protocol for requests?
        """
        self._auth = dict(
            api_id=api_id,
            user=user,
            password=password
        )
        self._https = https

        #: Provider API endpoint
        self._hostname = 'api.clickatell.com'

    def _api_request(self, method, **params):
        """ Make an API request and return the result

            :rtype: str
        """
        # Prepare the request
        url = '{schema}://{host}/http/{method}'.format(
            schema='https' if self._https else 'http',
            host=self._hostname,
            method=method
        )
        data = {}
        data.update(self._auth)
        data.update(params)
        post = urllib.urlencode(data)

        # Request
        req = urllib2.Request(url, post)
        res = urllib2.urlopen(req)
        return res.read()

    def api_request(self, method, **params):
        """ Make a custom request to Clickatell and get the response object.

            This also handles errors reported by the Clickatell API

            :type method: str
            :param method: Method name to call
            :param params: Method parameters to send
            :raises HTTPError: Http error code
            :raises URLError: Connection failed
            :raises ClickatellApiError: Clickatell error
        """
        response = self._api_request(method, **params)

        # Error?
        m = re.match(r'^ERR: (\d+), (.*)', response)
        if m:
            raise ClickatellApiError(code=int(m.group(1)), message=m.group(2))
        else:
            return response

    def getbalance(self):
        """ Query balance

            :rtype: float
            :returns: the number of credits available on this particular account.
        """
        response = self.api_request('getbalance')
        m = re.match(r'^Credit: ([\d\.]+)$', response)
        assert m is not None, 'Failed to parse response: {}'.format(response)
        return float(m.group(1))

    def sendmsg(self, to, text, **params):
        """ Send SMS message

            See :meth:`ClickatellHttpApi.api_request` for the list of raised exceptions.

            :param to: Destination number, digits only
            :param text: Message text: str or unicode.
            :param params: Message parameters. See Clickatell docs.

            :param from: Sender address: SenderID, or one of the registered outgoing phone numbers. Default: ''
            :param deliv_ack: Enable/disable delivery acknowledgements. 0|1. Default: 0
            :param callback: Callback URL for status reports. Receives data with HTTP GET. Default: None
            :param deliv_time: SMS delivery delay in minutes. Default: None
            :param escalate: High-pri message: can potentially choose pricier gateways but deliver faster. 0|1. Default: 0
            :param mo: Enable the ability to reply. 0|1. Default: 0.
            :param unicode: Enable unicode messages. If set to 1, the `text` should contain 2-byte unicode. Default: 0
            :param validity: Message validity (expire) period in minutes. Default: None
            :param req_feat: Required features list for the gateway: or'ed constants. see :class:`Features`

            :rtype: str
            :returns: Message id
        """
        # Recipient
        # TODO: Clickatell allows to specify multiple recipients, ','-separated. Implement it! ..and handle the multiple responses
        params['to'] = to

        # Param: `concat`: enable message concatenation.
        # Message length: 160 7bit chars || 140 8bit chars
        # Note: concatenation reduces each message by 7 chars
        concat_parts = (lambda n: 1 if n <= 140 else math.ceil(n/float(140-7)))(len(text.encode('utf-8')))
        if concat_parts > 1:
            params['concat'] = 1

        # CHECKME: seems like req_feat requires FEAT_DELIVACK to be set for acknowledgements. Check it!

        # Unicode message
        if len(text.encode('utf-8')) == len(text):
            params['text'] = str(text)
        else:
            # Unicode message
            params['unicode'] = 1
            params['text'] = binascii.hexlify(text.encode('UTF-16BE'))  # Convert to UCS-2 HEX (utf-16 big-endian)

        # Send it, parse the response
        response = self.api_request('sendmsg', **params)
        m = re.match(r'^ID: (.*)$', response)
        assert m is not None, 'Failed to parse response: {}'.format(response)
        return m.group(1)
