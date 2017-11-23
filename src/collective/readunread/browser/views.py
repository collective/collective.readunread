# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from collective.readunread.utils import current_userid
from collective.readunread.utils import set_ru_status
from z3c.json.interfaces import IJSONWriter
from zope.component import getUtility
# from zope.lifecycleevent import modified


class ReadUnreadView(BrowserView):

    def __call__(self):
        """ Change read/unread status """
        action = self.request.get('action', None)
        userid = current_userid()
        writer = getUtility(IJSONWriter)
        self.request.response.setHeader('content-type', 'application/json')
        json = {'ret': 'nok'}
        try:
            if action in ('mark_as_read', 'mark_as_unread'):
                action = action[8:]
                status = set_ru_status(self.context, userid=userid, status=action)
#                modified(self.context)
                json['ret'] = 'ok'
                json['status'] = status
        except Exception:
            pass
        return writer.write(json)
