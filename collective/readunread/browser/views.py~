try:
    import json
except ImportError:
    import simplejson as json

from zope import component

from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from collective.readunread.interfaces import IReadByProvider
from collective.readunread.interfaces import IReadByManager


class Helpers(BrowserView):
    """
    """

    @property
    def portal_state(self):
        return component.getMultiAdapter((self.context,self.request),
                                         name="plone_portal_state")

    def is_markable(self, obj=None, path=None, uid=None):
        """ returns ttrue iff an obj is markable as read/unread
        """
        if not obj:
            obj = self._getObject(path=path, uid=uid)
        return IReadByProvider.providedBy(obj)

    def _getObject(self, path=None, uid=None):
        if path:
            obj = self.context.restrictedTraverse(path)
        elif uid:
            catalog = getToolByName(self.context,'portal_catalog')
            brains = catalog(UID=uid)
            if brains:
                obj = brains[0].getObject()
        if obj:
            return obj
        else:
            raise LookupError("Can't find object!")

    def mark_as(self, obj=None, mark_as="read", userid=None, **kwargs):
        """ mark an object as read/unread
        """
        mark_as = self.request.get('mark_as',mark_as)
        userid = self.portal_state.member().getId()
        if not userid:
            pm = getToolByName(self.context,'portal_membership')
            member = pm.getAuthenticatedMember()
            userid = member.getId()
        assert mark_as and isinstance(mark_as,str)
        if not obj:
            key = {}
            for i in ['uid','path']:
                if self.request.get(i):
                    key[i] = self.request.get(i,kwargs.get(i))
            if key:
                obj = self._getObject(**key)
        if obj:
            manager = self.get_manager(obj)
            manager.set_as(mark_as, [userid,])
            marked_as = manager.get_status(userid)
            return json.dumps(dict(status='ok',marked_as=marked_as))
        return json.dumps(dict(status='fail',marked_as="nothing"))

    def get_status(self, obj):
        """ return the status of the obj
        """
        userid = self.portal_state.member().getId()
        return self.get_manager(obj).get_status(userid)

    def get_manager(self, obj):
        return IReadByManager(obj)
