# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.readunread.utils import get_ru_status
from collective.readunread.utils import set_ru_status
from collective.readunread.testing import COLLECTIVE_READUNREAD_INTEGRATION_TESTING  # noqa
from plone.app.testing import TEST_USER_ID

import unittest


class TestAdapters(unittest.TestCase):
    """Test collective.readunread adapters.py."""

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']
        self.pc = self.portal.portal_catalog

    def test_read_by_index(self):
        # test catalog search, also with 'not' query to find 'unread' items
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        self.assertEqual(len(self.pc(portal_type='testtype', read_by=0)), 1)
        self.assertEqual(len(self.pc(portal_type='testtype', read_by=TEST_USER_ID)), 0)
        self.assertEqual(len(self.pc(portal_type='testtype', read_by={'not': TEST_USER_ID})), 1)
        # change read status for current user id
        set_ru_status(self.tt1, status='read')
        self.assertEqual(len(self.pc(portal_type='testtype', read_by=0)), 0)
        self.assertEqual(len(self.pc(read_by=TEST_USER_ID)), 1)
        self.assertEqual(len(self.pc(portal_type='testtype', read_by={'not': TEST_USER_ID})), 0)
