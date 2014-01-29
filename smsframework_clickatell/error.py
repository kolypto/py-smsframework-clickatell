""" Clickatell error codes """

from smsframework.exc import *


class ClickatellProviderError(ProviderError):
    """ Base class for Clickatell errors

        The __new__ method provides factory behavior: on construct, it mutates to one of its subclasses.
    """
    code = None
    title = '(UNKNOWN ERROR CODE)'

    def __new__(cls, code, message=''):
        # Pick the appropriate class
        for E in cls.__subclasses__():
            if E.code == code:
                C = E
                break
        else:
            C = cls
        return super(ClickatellProviderError, cls).__new__(C, code, message)

    def __init__(self, code, message=''):
        self.code = code
        super(ClickatellProviderError, self).__init__(
            '#{}: {}: {}'.format(self.code, self.title, message)
        )


class E001(ClickatellProviderError, AuthError):
    code = 1
    title = 'Authentication failed'


class E002(ClickatellProviderError, AuthError):
    code = 2
    title = 'Unknown username or password'


class E003(ClickatellProviderError, RequestError):
    code = 3
    title = 'Session ID expired'


class E005(ClickatellProviderError, RequestError):
    code = 5
    title = 'Missing session ID'


class E007(ClickatellProviderError, AuthError):
    code = 7
    title = 'IP Lockdown violation'


class E101(ClickatellProviderError, RequestError):
    code = 101
    title = 'Invalid or missing parameters'


class E102(ClickatellProviderError, RequestError):
    code = 102
    title = 'Invalid user data header'


class E103(ClickatellProviderError, RequestError):
    code = 103
    title = 'Unknown API message ID'


class E104(ClickatellProviderError, RequestError):
    code = 104
    title = 'Unknown client message ID'


class E105(ClickatellProviderError, RequestError):
    code = 105
    title = 'Invalid destination address'


class E106(ClickatellProviderError, RequestError):
    code = 106
    title = 'Invalid source address'


class E107(ClickatellProviderError, RequestError):
    code = 107
    title = 'Empty message'


class E108(ClickatellProviderError, RequestError):
    code = 108
    title = 'Invalid or missing API ID'


class E109(ClickatellProviderError, RequestError):
    code = 109
    title = 'Missing message ID'


class E113(ClickatellProviderError, RequestError):
    code = 113
    title = 'Maximum message parts exceeded'


class E114(ClickatellProviderError, ServerError):
    code = 114
    title = 'Cannot route message'


class E115(ClickatellProviderError):
    code = 115
    title = 'Message expired'


class E116(ClickatellProviderError, RequestError):
    code = 116
    title = 'Invalid Unicode data'


class E120(ClickatellProviderError, RequestError):
    code = 120
    title = 'Invalid delivery time'


class E121(ClickatellProviderError):
    code = 121
    title = 'Destination mobile number blocked'


class E122(ClickatellProviderError):
    code = 122
    title = 'Destination mobile opted out'


class E123(ClickatellProviderError, RequestError):
    code = 123
    title = 'Invalid Sender ID'


class E128(ClickatellProviderError):
    code = 128
    title = 'Number delisted'


class E130(ClickatellProviderError, LimitsError):
    code = 130
    title = 'Maximum MT limit exceeded until <UNIX TIME STAMP>'


class E201(ClickatellProviderError, RequestError):
    code = 201
    title = 'Invalid batch ID'


class E202(ClickatellProviderError, RequestError):
    code = 202
    title = 'No batch template'


class E301(ClickatellProviderError, CreditError):
    code = 301
    title = 'No credit left'


class E901(ClickatellProviderError, ServerError):
    code = 901
    title = 'Internal error'
