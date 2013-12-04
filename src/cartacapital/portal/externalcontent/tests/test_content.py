# -*- coding: utf-8 -*-

from App.Common import package_home
from cartacapital.portal.externalcontent.content.blog import IExternalBlog
from cartacapital.portal.externalcontent.content.blog_entry import IExternalBlogEntry
from cartacapital.portal.externalcontent.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName
from zope.component import createObject
from zope.component import queryUtility

import unittest
import os


class ExternalBlogIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('ExternalBlog', 'blog')
        self.blog = self.folder['blog']

    def test_adding(self):
        self.assertTrue(IExternalBlog.providedBy(self.blog))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='ExternalBlog')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='ExternalBlog')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IExternalBlog.providedBy(new_object))


class ExternalBlogEntryIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('ExternalBlog', 'test-blog')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.blog = self.portal['test-blog']
        self.blog.invokeFactory('ExternalBlogEntry', 'post')
        self.post = self.blog['post']

    def test_adding(self):
        self.assertTrue(IExternalBlogEntry.providedBy(self.post))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='ExternalBlogEntry')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='ExternalBlogEntry')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IExternalBlogEntry.providedBy(new_object))

    def test_section(self):
        self.blog.section = u'Tommy'
        self.assertEqual(self.post.section, u'Tommy')


class ProcessFeedsIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('ExternalBlog', 'test-blog')
        self.blog = self.portal['test-blog']
        self.blog.remoteUrl = os.path.join(package_home(globals()), 'test_feed.rss')

    def test_view(self):
        self.assertEqual(len(self.blog.objectIds()), 0)
        self.blog.restrictedTraverse('@@processa-feeds')()
        self.assertEqual(len(self.blog.objectIds()), 10)
        self.assertIsNotNone(self.blog.get('pororoca'))

        self.blog.restrictedTraverse('@@processa-feeds')()
        self.assertEqual(len(self.blog.objectIds()), 10)

        workflowTool = getToolByName(self.portal, 'portal_workflow')
        ob = self.blog.get('pororoca')
        chain = workflowTool.getChainFor(ob)
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'simple_publication_workflow')

        status = workflowTool.getStatusOf('simple_publication_workflow', ob)
        state = status["review_state"]
        self.assertEqual(state, 'published')
