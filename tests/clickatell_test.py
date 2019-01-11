# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from flask import Flask

from smsframework import Gateway, OutgoingMessage
from smsframework.providers import NullProvider
from smsframework_clickatell import ClickatellProvider

from smsframework_clickatell import error, status


class ClickatellProviderTest(unittest.TestCase):
    def setUp(self):
        # Gateway
        gw = self.gw = Gateway()
        gw.add_provider('null', NullProvider)  # provocation
        gw.add_provider('main', ClickatellProvider, api_id=10, user='kolypto', password='1234')

        # Flask
        app = self.app = Flask(__name__)

        # Register receivers
        gw.receiver_blueprints_register(app, prefix='/a/b/')

    def _mock_response(self, response):
        """ Monkey-patch ClickatellHttpApi so it returns a predefined response """
        def _api_request(method, **params):
            return response
        self.gw.get_provider('main').api._api_request = _api_request

    def test_blueprints(self):
        """ Test blueprints """
        self.assertEqual(
            list(self.gw.receiver_blueprints().keys()),
            ['main']
        )

    def test_api_request(self):
        """ Test raw requests """
        provider = self.gw.get_provider('main')

        # OK
        self._mock_response('blah-blah')
        self.assertEqual(provider.api_request('hey'), 'blah-blah')

        # Error reported
        self._mock_response('ERR: 1, Auth fail')
        self.assertRaises(error.E001, provider.api_request, 'hey')

        # Error reported, unknown code
        self._mock_response('ERR: 999, Auth fail')
        self.assertRaises(error.ClickatellProviderError, provider.api_request, 'hey')


    def test_getbalance(self):
        """ Test getting balance """
        provider = self.gw.get_provider('main')

        # OK
        self._mock_response('Credit: 12.50')
        self.assertEqual(provider.getbalance(), 12.50)

        # Invalid response
        self._mock_response('blah-blah')
        self.assertRaises(AssertionError, provider.getbalance)

    def test_send(self):
        """ Test message send """
        gw = self.gw

        # OK
        self._mock_response('ID: 11111111')
        message = gw.send(OutgoingMessage('+123456', 'hey', provider='main'))
        self.assertEqual(message.msgid, '11111111')

        # Failure
        self._mock_response('ERR: 001, Auth fail')
        self.assertRaises(error.E001, gw.send, OutgoingMessage('+123456', 'hey', provider='main'))

    def test_receive_message(self):
        """ Test message receipt """

        # Message receiver
        messages = []
        def receiver(message):
            messages.append(message)
        self.gw.onReceive += receiver

        with self.app.test_client() as c:
            # Message 1: artificial
            res = c.get('/a/b/main/im'
                        '?api_id=100'
                        '&moMsgId=1'
                        '&from=123'
                        '&to=456'
                        '&timestamp=2008-08-06 09:43:50'
                        '&charset=ISO-8859-1'
                        '&text=hello there'
                        '&udh=')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(messages), 1)
            message = messages.pop()
            self.assertEqual(message.provider, 'main')
            self.assertEqual(message.msgid, '1')
            self.assertEqual(message.src, '123')
            self.assertEqual(message.dst, '456')
            self.assertEqual(message.body, 'hello there')
            self.assertEqual(message.rtime.strftime('%Y-%m-%d %H:%M:%S'), '2008-08-06 07:43:50')  # UTC
            self.assertEqual(message.meta, {'api_id': '100', 'charset': 'ISO-8859-1', 'udh': ''})

            # Message 2: real, non-unicode
            res = c.get('/a/b/main/im'
                        '?api_id=3460000'
                        '&from=380660000000'
                        '&to=491700000000'
                        '&timestamp=2014-01-29+02%3A08%3A30'
                        '&text=Hi%2C+man'
                        '&charset=ISO-8859-1'
                        '&udh='
                        '&moMsgId=c6b1e0eb9d6b8d549621235aaf089a26')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(messages), 1)
            message = messages.pop()
            self.assertEqual(message.provider, 'main')
            self.assertEqual(message.msgid, 'c6b1e0eb9d6b8d549621235aaf089a26')
            self.assertEqual(message.src, '380660000000')
            self.assertEqual(message.dst, '491700000000')
            self.assertEqual(message.body, 'Hi, man')
            self.assertEqual(message.rtime.strftime('%Y-%m-%d %H:%M:%S'), '2014-01-29 00:08:30')  # UTC
            self.assertEqual(message.meta, {'api_id': '3460000', 'charset': 'ISO-8859-1', 'udh': ''})

            # Message 3: real, unicode
            res = c.get('/a/b/main/im'
                        '?api_id=3460000'
                        '&from=380660000000'
                        '&to=491700000000'
                        '&timestamp=2014-01-29+02%3A05%3A46'
                        '&text=%04%1F%04%40%048%042%045%04B%00%2C%00+%046%04%3E%04%3F%040%00!'
                        '&charset=UTF-16BE'
                        '&udh='
                        '&moMsgId=1de97e5e15f76bb1e374f1ea3d33bf65')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(messages), 1)
            message = messages.pop()
            self.assertEqual(message.provider, 'main')
            self.assertEqual(message.msgid, '1de97e5e15f76bb1e374f1ea3d33bf65')
            self.assertEqual(message.src, '380660000000')
            self.assertEqual(message.dst, '491700000000')
            self.assertEqual(message.body, u'Привет, жопа!')  # sorry :)
            self.assertEqual(message.rtime.strftime('%Y-%m-%d %H:%M:%S'), '2014-01-29 00:05:46')  # UTC
            self.assertEqual(message.meta, {'api_id': '3460000', 'charset': 'UTF-16BE', 'udh': ''})

    def test_receive_status(self):
        """ Test status receipt """

        # Status receiver
        statuses = []

        def receiver(status):
            statuses.append(status)

        self.gw.onStatus += receiver

        with self.app.test_client() as c:
            # Status 1: artificial, accepted
            res = c.get('/a/b/main/status'
                        '?from=123'
                        '&to=456'
                        '&status=2'
                        '&api_id=100'
                        '&moMsgId=1'
                        '&charge=0.32')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(statuses), 1)
            st = statuses.pop()
            self.assertEqual(st.msgid, '1')
            self.assertEqual(st.rtime.strftime('%Y-%m-%d'), datetime.utcnow().strftime('%Y-%m-%d'))  # this test fails at midnight :)
            self.assertEqual(st.meta, {'status': 2, 'api_id': '100', 'charge': 0.32})
            self.assertEqual(st.provider, 'main')
            self.assertEqual(st.accepted, True)
            self.assertEqual(st.delivered, False)
            self.assertEqual(st.expired, False)
            self.assertEqual(st.status_code, 2)
            self.assertEqual(st.status, status.S002.status)
            self.assertEqual(st.error, False)

            # Status 2: artificial, delivered
            res = c.get('/a/b/main/status'
                        '?from=123'
                        '&to=456'
                        '&status=4'
                        '&api_id=100'
                        '&moMsgId=1'
                        '&charge=0.32')
            st = statuses.pop()
            self.assertEqual(st.accepted, True)
            self.assertEqual(st.delivered, True)
            self.assertEqual(st.expired, False)
            self.assertEqual(st.status_code, 4)
            self.assertEqual(st.status, status.S004.status)
            self.assertEqual(st.error, False)

            # Status 2: artificial, error
            res = c.get('/a/b/main/status'
                        '?from=123'
                        '&to=456'
                        '&status=5'
                        '&api_id=100'
                        '&moMsgId=1'
                        '&charge=0.32')
            st = statuses.pop()
            self.assertEqual(st.accepted, True)
            self.assertEqual(st.delivered, False)
            self.assertEqual(st.expired, False)
            self.assertEqual(st.status_code, 5)
            self.assertEqual(st.status, status.S005.status)
            self.assertEqual(st.error, True)
