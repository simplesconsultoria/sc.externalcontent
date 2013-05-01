# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.browserlayer.utils import registered_layers

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from cartacapital.portal.externalcontent.config import PROJECTNAME
from cartacapital.portal.externalcontent.testing import INTEGRATION_TESTING


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IExternalContentLayer' in layers,
                        'add-on layer was not installed')


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IExternalContentLayer' not in layers,
                        'add-on layer was not removed')
