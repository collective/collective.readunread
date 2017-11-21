# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.readunread.testing import COLLECTIVE_READUNREAD_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.readunread is properly installed."""

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.readunread is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.readunread'))

    def test_browserlayer(self):
        """Test that ICollectiveReadunreadLayer is registered."""
        from collective.readunread.interfaces import (
            ICollectiveReadunreadLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveReadunreadLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_READUNREAD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.readunread'])

    def test_product_uninstalled(self):
        """Test if collective.readunread is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.readunread'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveReadunreadLayer is removed."""
        from collective.readunread.interfaces import \
            ICollectiveReadunreadLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveReadunreadLayer, utils.registered_layers())
