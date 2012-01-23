from zope.i18nmessageid import MessageFactory

ReadUnreadMF = MessageFactory("collective.readunread")
_ = ReadUnreadMF

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
