# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.readunread.browser import viewlets
# from collective.readunread.browser.viewlets import ReadUnreadViewlet
from collective.readunread.utils import get_ru_status
from collective.readunread.testing import COLLECTIVE_READUNREAD_INTEGRATION_TESTING  # noqa
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import unittest


class TestReadUnreadViewlet(unittest.TestCase):
    """Test collective.readunread viewlets.py."""

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']

    def test_viewlet(self):
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        viewlet = viewlets.ReadUnreadViewlet(self.tt1, self.tt1.REQUEST, None)
        # test status
        self.assertEqual(viewlet.get_status(), 'unread')
        # test availability
        self.assertTrue(viewlet.available())
        # test rendering
        pt = ViewPageTemplateFile('read_unread_by_member.pt', _prefix={'__file__': viewlets.__file__})
        ret = pt(viewlet)
        self.assertIn('id="read_unread_viewlet"', ret)
