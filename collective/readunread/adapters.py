from zope import interface
from zope import component

from collective.readunread.interfaces import IReadByProvider
from collective.readunread.interfaces import IReadByManager
from collective.readunread.myutils import set_readby
from collective.readunread.myutils import set_unreadby
from collective.readunread.myutils import get_status


class Manager(object):
    """ adapter for managing readby values all in one
    """

    interface.implements(IReadByManager)
    component.adapts(IReadByProvider)

    def __init__(self, context):
        self.context = context

    def set_readby(self, userids):
        set_readby(self.context,userids=userids)

    def set_unreadby(self, userids):
        set_unreadby(self.context,userids=userids)

    def set_as(self, status, userids):
        if status == 'read':
            self.set_readby(userids)
        elif status == 'unread':
            self.set_unreadby(userids)

    def get_readby(self):
        get_readby(self.context)

    def get_status(self,userid):
        return get_status(self.context,userid)
