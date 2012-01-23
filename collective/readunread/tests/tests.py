"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for
example.
"""

import unittest
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.PloneTestCase import PloneTestCase
from Products.Five.testbrowser import Browser
from Products.Five import zcml

from zope import interface
from zope.event import notify
from zope.publisher.browser import TestRequest

from plone.validatehook.event import PostValidationEvent
from Products.Archetypes.event import ObjectInitializedEvent

from collective.readunread.extender import READBY_FIELDNAME
from collective.readunread.myutils import get_readby
from collective.readunread.myutils import set_readby
from collective.readunread.myutils import set_unreadby
from collective.readunread.interfaces import IReadByProvider
from collective.readunread.tests import base


configure_zcml = """
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:five="http://namespaces.zope.org/five"
    i18n_domain="foo">

    <five:implements
      class="Products.ATContentTypes.content.document.ATDocument"
      interface="collective.readunread.interfaces.IReadByProvider"
      />

</configure>"""


def fireViewEvent(obj, userid):
    request = TestRequest()
    user = getToolByName(obj,'acl_users').getUserById(userid)
    event = PostValidationEvent(obj,request,user)
    notify(event)

def addMember(portal, username, fullname="", email="", roles=('Member',), last_login_time=None):
    portal.portal_membership.addMember(username, 'secret', roles, [])
    member = portal.portal_membership.getMemberById(username)
    member.setMemberProperties({'fullname': fullname, 'email': email,
                                'last_login_time': DateTime(last_login_time),})

def setupMembers(portal, n=5):
    for i in range(1,n+1):
        userid = 'user%s' % i
        fullname = 'User %s Fullname' % i
        email = 'user%s@email.com' % i
        addMember(portal,userid,fullname=fullname,email=email)


class TestSetup(base.TestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    readby_fieldname = READBY_FIELDNAME

    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        zcml.load_string(configure_zcml)
        self.setRoles(['Manager', 'Member'])
        self.portal.invokeFactory('Folder','folder')
        self.folder = self.portal['folder']
        self.folder.invokeFactory('Document','document')
        self.obj = self.folder['document']
        interface.alsoProvides(self.obj,IReadByProvider)
        setupMembers(self.portal)

    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
        self.deleteObj()

    def deleteObj(self):
        self.folder._delObject(self.obj.getId())

    def test_install_dependencies(self):
        pass

    js_res_basepath = "++resource++"
    js_files = ['readunread.js', ]

    def test_portal_js(self):
        tool = getToolByName(self.portal,'portal_javascripts')
        for name in self.js_files:
            self.failUnless(self.js_res_basepath + name in tool.getResourceIds(),
                            "%s not found in %s" % (name, tool.getId())
                            )

    css_res_basepath = "++resource++"
    css_files = ['readunread.css', ]

    def test_portal_css(self):
        p_css = getToolByName(self.portal,'portal_css')
        for css_name in self.css_files:
            self.failUnless(self.css_res_basepath + css_name in p_css.getResourceIds(),
                            "%s not found in portal_css" % css_name)


    def test_readby_interface(self):
        self.failUnless(IReadByProvider.providedBy(self.obj))

    def test_readby_field(self):
        # we must not trigger AT events to keep default values
        schema = self.obj.Schema()

        # check for field into schema
        self.failUnless(self.readby_fieldname in schema.keys())

        # check field type
        field = schema.getField(self.readby_fieldname)
        self.assertEqual(field.type,'lines')

        # default value should be an empty tuple
        field_value = field.get(self.obj)
        self.assertEqual(field_value,())

    def test_get_and_set(self):
        username = PloneTestCase.default_user
        # login as simple user
        self.login(username)
        set_readby(self.obj)
        readby = get_readby(self.obj)
        self.failUnless(username in readby)

    def test_readby_catalog_index(self):
        # check index existence
        ct = getToolByName(self.portal, 'portal_catalog')
        self.failUnless('readBy' in ct.indexes())

        # check indexed value
        username = "johndoe"
        set_readby(self.obj,userids=[username])
        self.obj.reindexObject()
        brains = ct(readBy=username)
        self.failUnless(len(brains)==1)

    def test_readby_creator(self):
        username = PloneTestCase.default_user
        # login as simple user
        self.login(username)
        # create the object
        self.folder.invokeFactory('Document','document1')
        obj = self.folder['document1']
        # fire event
        notify(ObjectInitializedEvent(obj))
        creator = obj.Creator()
        readby = get_readby(obj)
        # creator's id must be into readby users
        self.failUnless(username in readby)

    def test_readby_view_event(self):
        fireViewEvent(self.obj,'user1')
        assert 'user1' in get_readby(self.obj)

        fireViewEvent(self.obj,'user2')
        assert 'user2' in get_readby(self.obj)

        userids = ['user1',
                   'user2',]
        readby = list(get_readby(self.obj))
        readby.sort()
        self.assertEquals(userids,readby)

    def test_set_unreadby(self):
        for x in range(1,5):
            fireViewEvent(self.obj,'user%s' % x)
        # check users
        assert 'user1' in get_readby(self.obj)
        assert 'user2' in get_readby(self.obj)
        # remove some users
        set_unreadby(self.obj, ['user1','user2'])
        assert 'user1' not in get_readby(self.obj)
        assert 'user2' not in get_readby(self.obj)
        # other users are still there
        assert 'user3' in get_readby(self.obj)
        assert 'user4' in get_readby(self.obj)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
