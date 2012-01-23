# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.Archetypes import atapi

from collective.readunread.interfaces import IReadByProvider

from collective.readunread import _

READBY_FIELDNAME = 'readBy'


class ReadByField(ExtensionField, atapi.LinesField):
    """ read/unread field """

class BaseExtender(object):

    implements(ISchemaExtender)

    fields = []

    def __init__(self, context):
         self.context = context

    def getFields(self):
        return self.fields


class ReadByExtender(BaseExtender):
    adapts(IReadByProvider)

    fields = [
        ReadByField(
            READBY_FIELDNAME,
            storage = atapi.AnnotationStorage(),
            widget = atapi.LinesWidget(
                label=_(u"Read by"),
                description=_(u"Contains the list of users' ids that read the object"),
                visible={'view':'invisible','edit':'invisible'},
            ),
        ),
    ]
