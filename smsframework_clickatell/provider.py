from smsframework import IProvider, exc
from . import error
from . import status
from .api import ClickatellHttpApi, ClickatellApiError
from urllib2 import URLError, HTTPError


class ClickatellProvider(IProvider):
    """ Clickatell provider """

    def __init__(self, gateway, name, api_id, user, password, https=False):
        """ Configure Clickatell provider

            :param api_id: API ID to use
            :param user: Account username
            :param password: Account password
            :param https: Use HTTPS for outgoing messages?
        """
        self.api = ClickatellHttpApi(api_id, user, password, https)
        super(ClickatellProvider, self).__init__(gateway, name)

    def send(self, message):
        """ Send a message

            :type message: smsframework.data.OutgoingMessage.OutgoingMessage
            :rtype: OutgoingMessage
            """
        # Parameters
        params = {}
        if message.src:
            params['from'] = message.src
        if message.provider_options.status_report:
            params['deliv_ack'] = 1
        if message.provider_options.escalate:
            params['escalate'] = 1
        if message.provider_options.allow_reply:
            params['mo'] = 1
        if message.provider_options.expires:
            params['validity'] = message.provider_options.expires
        if message.provider_options.senderId:
            params['from'] = message.provider_options.senderId
        params.update(message.provider_params)

        # Send
        try:
            message.msgid = self.api.sendmsg(message.dst, message.body, **params)
            return message
        except HTTPError as e:
            raise exc.MessageSendError(e.message)
        except URLError as e:
            raise exc.ConnectionError(e.message)
        except ClickatellApiError as e:
            raise error.ClickatellProviderError(e.code, e.message)  # will mutate into the necessary error object

    def make_receiver_blueprint(self):
        """ Create the receiver blueprint

            We do it in a function as the SmsFramework user might not want receivers, consequently, has no reasons
            for installing Flask
        """
        from . import receiver
        return receiver.bp

    #region Public

    def api_request(self, method, **params):
        """ Raw request to Clickatell API

            :rtype: str
            :raises ConnectionError: Connection error
            :raises MessageSendError: HTTP error
            :raises ClickatellProviderError: Error with the request
        """
        try:
            return self.api.api_request(method, **params)
        except HTTPError as e:
            raise exc.MessageSendError(e.message)
        except URLError as e:
            raise exc.ConnectionError(e.message)
        except ClickatellApiError as e:
            raise error.ClickatellProviderError(e.code, e.message)  # will mutate into the necessary error object

    def getbalance(self):
        """ Query balance

            :rtype: float
            :returns: The number of credits available
        """
        try:
            return self.api.getbalance()
        except HTTPError as e:
            raise exc.MessageSendError(e.message)
        except URLError as e:
            raise exc.ConnectionError(e.message)
        except ClickatellApiError as e:
            raise error.ClickatellProviderError(e.code, e.message)

    #endregion
