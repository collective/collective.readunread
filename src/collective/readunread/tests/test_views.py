# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.readunread.utils import get_ru_status
from collective.readunread.testing import COLLECTIVE_READUNREAD_INTEGRATION_TESTING  # noqa

import unittest


class TestReadUnreadView(unittest.TestCase):
    """Test collective.readunread views.py."""

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']

    def test_read_unread_view(self):
        self.assertEqual(get_ru_status(self.tt1), 'unread')
        view = self.tt1.restrictedTraverse('change_read_unread_status')
        # no action defined
        self.assertEqual(view(), u'{"ret":"nok"}')
        # action is mark_as_read
        view.request.set('action', 'mark_as_read')
        ret = view()
        self.assertIn('"status":"read"', ret)
        self.assertIn('"ret":"ok"', ret)
        self.assertEqual(get_ru_status(self.tt1), 'read')
        # action is mark_as_unread
        view.request.set('action', 'mark_as_unread')
        ret = view()
        self.assertIn('"status":"unread"', ret)
        self.assertIn('"ret":"ok"', ret)
        self.assertEqual(get_ru_status(self.tt1), 'unread')
