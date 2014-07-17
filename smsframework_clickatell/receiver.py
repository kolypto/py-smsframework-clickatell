from datetime import datetime, timedelta

from flask import Blueprint
from flask.globals import request, g

from smsframework.data import IncomingMessage
from .status import ClickatellMessageStatus

bp = Blueprint('smsframework-clickatell', __name__, url_prefix='/')


def _merge_request(request):
    """ Merge query string and form body """
    data = {}
    data.update(request.form.to_dict())
    data.update(request.args.to_dict())
    return data


@bp.route('/im', methods=['GET', 'POST'])
def im():
    """ Incoming message handler

        Clickatell sends data with either GET or POST:

        * api_id: Api ID
        * moMsgId: MO message ID
        * from: Originating ISDN
        * to: Destination ISDN
        * timestamp: Date & Time in MySQL format, GMT+0200: "2008-08-06 09:43:50"
        * charset: DCS Character Coding [when applicable]
        * udh: Header Data [e.g. UDH etc.] [when applicable]
        * text: Message Data
    """
    req = _merge_request(request)

    # Check fields
    for n in ('api_id', 'moMsgId', 'from', 'to', 'timestamp', 'charset', 'udh', 'text'):
        assert n in req, 'Clickatell sent a message with missing "{}" field: {}'.format(n, req)

    # Parse date
    rtime = datetime.strptime(req['timestamp'], '%Y-%m-%d %H:%M:%S')
    rtime -= timedelta(hours=2)  # Date is in GMT+0200. Alter it to UTC

    # Message encoding
    req['text'] = req['text'].decode(req['charset'])

    # IncomingMessage
    message = IncomingMessage(
        src=req['from'],
        body=req['text'],  # CHECKME: test that unicode works
        msgid=req['moMsgId'],
        dst=req['to'],
        rtime=rtime,
        meta={
            'api_id': req['api_id'],
            'charset': req['charset'],
            'udh': req['udh']
        }
    )

    # Process it
    provider = g.provider  # yes, this is how the current provider is fetched
    " :type: smsframework.IProvider.IProvider "
    provider._receive_message(message)  # any exceptions will respond with 500, and Clickatell will happily retry later

    # Ack
    return 'OK'  # Clickatell protocol is well-structured, yes


@bp.route('/status', methods=['GET', 'POST'])
def status():
    """ Incoming status report

         Clickatell sends data with either GET or POST:

         * from: source number
         * to: destination number
         * status: status code
         * cliMsgId: client-specified msgid (if provided)
         * api_id: API id
         * moMsgId: msgid
         * charge: charged credits
    """
    req = _merge_request(request)

    # Check fields
    for n in ('from', 'to', 'status', 'api_id', 'moMsgId', 'charge'):
        assert n in req, 'Clickatell sent a status with missing "{}" field: {}'.format(n, req)

    # MessageStatus
    status = ClickatellMessageStatus.from_code(
        int(req['status']),
        msgid=req['moMsgId'],
        meta={
            'status': int(req['status']),
            'api_id': req['api_id'],
            'charge': float(req['charge'])
        }
    )

    # Process it
    g.provider._receive_status(status)  # exception respond with http 500

    # Ack
    return 'OK'
