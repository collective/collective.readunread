# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.readunread.utils import ANNOT_KEY
from collective.readunread.utils import current_userid
from collective.readunread.utils import get_ru_status
from collective.readunread.utils import set_ru_status
from collective.readunread.testing import COLLECTIVE_READUNREAD_INTEGRATION_TESTING  # noqa
from imio.helpers.content import add_to_annotation
from imio.helpers.content import del_from_annotation
from plone.app.testing import TEST_USER_ID

import unittest


class TestUtils(unittest.TestCase):
    """Test collective.readunread utils.py."""

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']

    def test_current_userid(self):
        self.assertEqual(current_userid(), TEST_USER_ID)

    def test_get_ru_status(self):
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        add_to_annotation(ANNOT_KEY, TEST_USER_ID, obj=self.tt1)
        self.assertEqual(get_ru_status(self.tt1), 'read')
        del_from_annotation(ANNOT_KEY, TEST_USER_ID, obj=self.tt1)
        self.assertEqual(get_ru_status(self.tt1), 'unread')

    def test_set_ru_status(self):
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        self.assertEqual(set_ru_status(self.tt1, status='read'), 'read')
        self.assertEqual(get_ru_status(self.tt1), 'read')
        self.assertEqual(set_ru_status(self.tt1, status='unread'), 'unread')
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        self.assertEqual(set_ru_status(self.tt1, status='unread'), 'unread')
