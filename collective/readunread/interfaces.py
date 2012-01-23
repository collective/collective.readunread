from zope import interface

class IReadByProvider(interface.Interface):
    """ marker interface for readBy field provider
    """

class IReadByManager(interface.Interface):
    """ adapter for handling read/unread status
    """
