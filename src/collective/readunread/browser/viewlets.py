# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from collective.readunread.utils import get_ru_status


class ReadUnreadViewlet(ViewletBase):
    """This viewlet displays available documents to generate."""

    def available(self):
        return True

    def get_status(self):
        return get_ru_status(self.context)
