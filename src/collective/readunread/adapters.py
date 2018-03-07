# -*- coding: utf-8 -*-

from collective.readunread.utils import ANNOT_KEY
from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from imio.helpers.content import get_from_annotation


@indexer(IContentish)
def read_by_index(obj):
    """ Index method escaping acquisition """
    userids = list(get_from_annotation(ANNOT_KEY, obj=obj, default=[]))
    # we need to put a default value not empty, because an empty list is not searched with 'not' query
    if not userids:
        userids = [0]
    return userids
