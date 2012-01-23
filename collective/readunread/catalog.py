from plone.indexer import indexer

from collective.readunread.interfaces import IReadByProvider
from collective.readunread.extender import READBY_FIELDNAME


def getFieldValue(obj,name):
    return obj.getField(name).get(obj)

@indexer(IReadByProvider)
def readBy(obj):
    return getFieldValue(obj,READBY_FIELDNAME)