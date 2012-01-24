collective.readunread
=====================

Introduction
============

This package provides read/unread status for Plone objects.

It adds a "readBy" field and a proper index to any object marked with IReadByProvider interface.


How to use it
=============

In order to activate read/unread feature the target object must implement::

    collective.readunread.interfaces.IReadByProvider


You can add a ZCML slug in your package like::

    <five:implements
      class="Products.ATContentTypes.content.document.ATDocument"
      interface="collective.readunread.interfaces.IReadByProvider"
      />


How it works
============

For testing purpose we'll assign it to the Document content type

>>> from zope import interface
>>> from Products.ATContentTypes.content.document import ATDocument
>>> from collective.readunread.interfaces import IReadByProvider
>>> interface.classImplements(ATDocument,IReadByProvider)

and create a Document

>>> self.setRoles(('Manager',))
>>> docid = self.folder.invokeFactory('Document', 'document')
>>> doc = self.folder[docid]

We must trigger IObjectInitializedEvent on it since we have a subcriber that
will take care of pushing the userid of the creator into 'readBy' field

>>> from Products.Archetypes.event import ObjectInitializedEvent
>>> from zope.event import notify
>>> notify(ObjectInitializedEvent(doc))

We can use the manager adapter for handling readby status

>>> from collective.readunread.interfaces import IReadByManager
>>> manager = IReadByManager(doc)

Since the doc is new we should get only creator's ID

>>> len(manager.get_readby()) == 1
True
>>> manager.get_readby()
('test_user_1_',)

Let's read the doc as other users. The following will create 3 new users

>>> from collective.readunread.tests.tests import setupMembers
>>> setupMembers(self.portal, n=3)

We have two ways for setting the doc as 'read' by a user. First, we can trigger
the PostValidationHook event with the user (that simulates viewing the doc)

>>> from collective.readunread.tests.tests import fireViewEvent
>>> fireViewEvent(doc,'user1')
>>> fireViewEvent(doc,'user2')

Let's see who read the doc

>>> 'user1' in manager.get_readby()
True
>>> 'user2' in manager.get_readby()
True
>>> 'user3' in manager.get_readby()
False

The second way is to set it trough the manager

>>> manager.set_readby(['user3',])
>>> 'user3' in manager.get_readby()
True

We can check the status of a user

>>> manager.get_status('user3')
'read'

We can also set a user as unread

>>> manager.set_unreadby(['user3',])
>>> 'user3' not in manager.get_readby()
True
>>> manager.get_status('user3')
'unread'


TODO
====

- document & test buttons macro
- document & test helper views