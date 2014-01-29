""" Message status codes """

from smsframework.data import *


class ClickatellMessageStatus(MessageStatus):
    status_code = None
    status = '(UNKNOWN STATUS CODE)'

    @classmethod
    def from_code(cls, status_code, **kwargs):
        """ Instantiate one of subclasses by code

            :rtype: type
        """
        for C in cls.__subclasses__():
            if C.status_code == status_code:
                return C(**kwargs)
        return cls(**kwargs)


class S001(ClickatellMessageStatus):
   status_code = 1
   status = 'Message unknown'


class S002(ClickatellMessageStatus, MessageAccepted):
   status_code = 2
   status = 'Message queued'


class S003(ClickatellMessageStatus, MessageAccepted):
   status_code = 3
   status = 'Delivered to gateway'


class S004(ClickatellMessageStatus, MessageDelivered):
   status_code = 4
   status = 'Received by recipient'


class S005(ClickatellMessageStatus, MessageError):
   status_code = 5
   status = 'Error with message'


class S006(ClickatellMessageStatus, MessageError):
   status_code = 6
   status = 'User cancelled message delivery'


class S007(ClickatellMessageStatus, MessageError):
   status_code = 7
   status = 'Error delivering message'


class S008(ClickatellMessageStatus, MessageAccepted):
   status_code = 8
   status = 'OK'


class S009(ClickatellMessageStatus, MessageError):
   status_code = 9
   status = 'Routing error'


class S010(ClickatellMessageStatus, MessageExpired):
   status_code = 10
   status = 'Message expired'


class S011(ClickatellMessageStatus, MessageAccepted):
   status_code = 11
   status = 'Message queued for later delivery'


class S012(ClickatellMessageStatus, MessageError):
   status_code = 12
   status = 'Out of credit'


class S014(ClickatellMessageStatus):
   status_code = 14
   status = 'Maximum MT limit exceeded'
