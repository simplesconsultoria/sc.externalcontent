# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from cartacapital.portal.externalcontent.config import TEMPLATE
from cartacapital.portal.externalcontent.content import blog
from five import grok
from Products.CMFCore.utils import getToolByName
from urllib2 import HTTPError
from urllib2 import urlopen
from zope.component import getMultiAdapter


grok.templatedir('templates')
STATUS_IMG = '%s/++resource++cartacapital.portal.externalcontent/%s.png'


class BlogView(grok.View):
    grok.context(blog.IExternalBlog)
    grok.name('blog_view')

    def update(self):
        """Redirect to the blog home if user is not able
           to edit it
        """
        context = self.context
        mtool = getToolByName(context, 'portal_membership')

        can_edit = mtool.checkPermission('Modify portal content', context)

        if not can_edit:
            url = context.siteUrl
            return context.REQUEST.RESPONSE.redirect(url)

    def render(self):
        return self.context.restrictedTraverse('folder_summary_view')()


class ConfigView(grok.View):
    grok.context(blog.IExternalBlog)
    grok.name('config')

    def update(self):
        ''' Configs '''
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.portal_url = portal_state.portal_url()
        self.partner = context.getId()
        self.section = context.section
        self.url = context.siteUrl
        self._process_site()
        self.domain_status = self._domain_status()
        self.ads_status = self._ads_status()
        self.bar_status = self._bar_status()

    def javascript(self):
        ''' '''
        return TEMPLATE % (self.partner, self.section)

    def _process_site(self):
        try:
            fh = urlopen(self.url)
        except HTTPError:
            # Error
            self.site_url = ''
            self.site_data = ''
        else:
            self.site_url = fh.url
            self.site_data = fh.read()
            fh.close()

    def _domain_status(self):
        ''' Check if site is on cartacapital.com.br domain '''
        status = 'cartacapital.com.br' in self.site_url
        self.domain_status_image = STATUS_IMG % (self.portal_url,
                                                 status and 'green' or 'red')
        return status and 'Ok' or 'Problemas'

    def _ads_status(self):
        ''' Check if ads (anuncios) are installed '''
        status = True
        expected = 'div-gpt-ad-1370011663251-0'
        status = expected in self.site_data
        self.ads_status_image = STATUS_IMG % (self.portal_url,
                                              status and 'green' or 'red')
        return status and 'Ok' or 'Problemas'

    def _bar_status(self):
        ''' Check if bar (barra) is installed '''
        status = True
        expected = 'js.cartacapital.com.br/barra.js'
        status = expected in self.site_data
        self.bar_status_image = STATUS_IMG % (self.portal_url,
                                              status and 'green' or 'red')
        return status and 'Ok' or 'Problemas'
