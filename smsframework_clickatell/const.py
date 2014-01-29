class Features:
    """ Outgoing message features

        These are OR'ed and provided as the :`OutgoingMessage.feat` message parameter
    """

    #: Text - set by default.
    FEAT_TEXT = 1

    #: 8-bit messaging - set by default.
    FEAT_8BIT = 2

    #: UDH (Binary) - set by default.
    FEAT_UDH = 4

    #: UCS2 / Unicode - set by default.
    FEAT_UCS2 = 8

    #: Alpha source address (from parameter).
    FEAT_ALPHA = 16

    #: Numeric source address (from parameter).
    FEAT_NUMER = 32

    #: Flash messaging.
    FEAT_FLASH = 512

    #: Delivery acknowledgments.
    FEAT_DELIVACK = 8192

    #: Concatenation - set by default.
    FEAT_CONCAT = 16384

    #: The default set of features
    DEFAULT = FEAT_TEXT | FEAT_8BIT | FEAT_UDH | FEAT_UCS2 | FEAT_CONCAT
