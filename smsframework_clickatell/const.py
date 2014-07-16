class Features:
    """ Outgoing message features

        These are OR'ed and provided as the :`OutgoingMessage.feat` message parameter
    """

    #: Text - set by default.
    FEAT_TEXT = 1 # 0x0001

    #: 8-bit messaging - set by default.
    FEAT_8BIT = 2 # 0x0002

    #: UDH (Binary) - set by default.
    FEAT_UDH = 4 # 0x0004

    #: UCS2 / Unicode - set by default.
    FEAT_UCS2 = 8 # 0x0008

    #: Alpha source address (from parameter).
    FEAT_ALPHA = 16 # 0x0010

    #: Numeric source address (from parameter).
    FEAT_NUMER = 32 # 0x0020

    #: Flash messaging.
    FEAT_FLASH = 512 # 0x0200

    #: Delivery acknowledgments.
    FEAT_DELIVACK = 8192 # 0x2000

    #: Concatenation - set by default.
    FEAT_CONCAT = 16384 # 0x4000

    #: The default set of features: 16399 = 0x400f
    DEFAULT = FEAT_TEXT | FEAT_8BIT | FEAT_UDH | FEAT_UCS2 | FEAT_CONCAT
