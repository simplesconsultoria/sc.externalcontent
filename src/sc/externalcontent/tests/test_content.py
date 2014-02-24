# -*- coding: utf-8 -*-

from App.Common import package_home
from sc.externalcontent.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.externalcontent.interfaces import ISCExternalContentSettings
from zope.component import getUtility

import unittest
import os


class ProcessFeedsIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = api.portal.get_tool(name='portal_catalog')
        wf_tool = api.portal.get_tool(name='portal_workflow')
        wf_tool.setDefaultChain('plone_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISCExternalContentSettings)
        settings.rss_sources = [u'test1,{0},test'.format(
                                os.path.join(package_home(globals()),
                                             'test_feed.rss'))]

    def test_view(self):
        self.assertEqual(len(self.catalog(portal_type='News Item')), 0)
        self.portal.restrictedTraverse('@@processa-feeds')()
        self.assertEqual(len(self.catalog(portal_type='News Item')), 10)
        self.portal.restrictedTraverse('@@processa-feeds')()
        self.assertEqual(len(self.catalog(portal_type='News Item')), 10)
