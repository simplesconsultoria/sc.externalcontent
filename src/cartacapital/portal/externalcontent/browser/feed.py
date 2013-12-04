# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from cartacapital.portal.externalcontent.content import blog
from cartacapital.portal.externalcontent.utils import str_to_datetime
from cartacapital.portal.externalcontent.utils import unescape
from datetime import datetime
from DateTime import DateTime
from five import grok
from lxml.cssselect import CSSSelector
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import _createObjectByType
from urllib2 import URLError
from urllib2 import Request
from urllib2 import urlopen
from zope.component import getMultiAdapter

import feedparser
import logging
import lxml.html
import time


log = logging.getLogger('cartacapital.portal.externalcontent')

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


class ProcessFeeds(grok.View):
    grok.context(blog.IExternalBlog)
    grok.name('processa-feeds')

    def __init__(self, context, request):
        super(ProcessFeeds, self).__init__(context, request)
        self.context = aq_inner(context)
        tools = getMultiAdapter((context, request), name=u'plone_tools')
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        self._portal = portal_state.portal()
        self._putils = self._portal.plone_utils
        self._ptransforms = self._portal.portal_transforms
        self._portal_url = portal_state.navigation_root_url()
        self._mt = tools.membership()
        self._portalPath = '/'.join(self._portal.getPhysicalPath())
        self._ct = tools.catalog()
        self._wt = tools.workflow()

    def render(self, *args, **kwargs):
        ''' Processa a lista de feeds '''
        member = self._mt.getAuthenticatedMember()
        self._username = member and member.getUserName() or ''
        self.processa_feed()
        url = self.context.absolute_url()
        return self.context.REQUEST.RESPONSE.redirect(url)

    def _getFeed(self, url):
        ''' Retorna feed processado'''
        data = feedparser.parse(url)
        return data

    def _feedItemsToNews(self, item, feedName):
        ''' Processa um item e retorna um dicionario contendo os campos de
            um News Item
        '''
        if not item:
            return
        pt = self._ptransforms
        dictNews = {'id': '',
                    'title': '',
                    'description': '',
                    'text': '',
                    'subjects': [],
                    'creators': [],
                    'rights': '',
                    'source': '',
                    'effectiveDate': '',
                    'creation_date': ''}

        now = datetime.now().timetuple()
        dictNews['title'] = item.get('title', '')
        # id deve ser uma string
        entry_id = str(self._putils.normalizeString('%s' % dictNews['title']))
        if entry_id in self.context.objectIds():
            # Content already there, ignore it
            return {}
        dictNews['id'] = entry_id
        description = item.get('summary', '')
        text = ''
        content = item.get('content', [{}, ])
        if 'value' in content[0]:
            text = content[0].value
        description_type = item.get('summary_detail', {}).get('type',
                                                              'text/plain')
        # Convert br tags to line breaks
        description = description.replace('<br />', '\n').encode('utf-8')
        description = pt.convertTo('text/plain', description,
                                   mimetype=description_type).getData()
        description = description.replace('&nbsp;', ' ')
        description = description.strip()
        if description:
            # If we have multiple paragraphs, get just the first one
            description = [l.strip() for l in description.split('\n')
                           if l.strip()][0]
        dictNews['description'] = unescape(description).decode('utf-8')
        dictNews['text'] = text
        image = self._image_from_body(text)
        if image:
            dictNews['image'] = image
            dictNews['image_caption'] = ''
        tags = item.get('tags', []) and [tag.get('term', '')
                                         for tag in item.get('tags', [])] or []
        dictNews['subjects'] = tags
        dictNews['creators'] = tuple([item.get('author', '') or feedName])
        dictNews['rights'] = feedName
        creation_date = (item.get('created_parsed', '') or
                         item.get('published_parsed', '') or
                         item.get('updated_parsed', now))
        dictNews['creation_date'] = str_to_datetime(
            creation_date and time.strftime('%Y-%m-%d %H:%M', creation_date))
        effectiveDate = item.get('published_parsed', '') or creation_date
        dictNews['effective_date'] = str_to_datetime(
            effectiveDate and time.strftime('%Y-%m-%d %H:%M', effectiveDate))
        dictNews['anexos'] = item.get('enclosures', [])
        dictNews['remoteUrl'] = item.get('feedburner_origlink',
                                         item.get('link', ''))
        if not dictNews['id']:
            dictNews = None
        return dictNews

    def _image_from_body(self, text):
        ''' Get the first image from entry body '''
        if not text:
            return None
        dom = lxml.html.fromstring(text)
        selAnchor = CSSSelector('img')
        foundElements = selAnchor(dom)
        links = [e.get('src') for e in foundElements]
        if links:
            link = links[0]
            req = Request(link.encode('utf-8'), headers=HDR)
            try:
                fh = urlopen(req)
            except URLError:
                # Not able to open the link
                # return an empty image
                return None
            data = fh.read()
            content_type = fh.headers['content-type']
            return (data, content_type)

    def _objFromUID(self, uid):
        ''' Return a object from an UID '''
        ct = self._ct
        results = ct.searchResults(UID=uid)
        if results:
            obj = results[0].getObject()
            return obj

    def create_entry(self, folder, dictNews):
        ''' Cria news item, realiza transição '''
        wt = self._wt
        oId = str(dictNews.get('id'))
        if not oId in folder.objectIds():
            _createObjectByType('ExternalBlogEntry', folder, id=oId,
                                title=dictNews.get('title'),
                                description=dictNews.get('description'))
        else:
            return folder[oId]
        log.info('     - Cria item %s' % (oId))
        o = folder[oId]
        if not o:
            return
        for k, v in dictNews.items():
            if k in ['title', 'id', 'anexos']:
                continue
            if k in ['text']:
                v = RichTextValue(v, 'text/html', 'text/html')
                o.text = v
            if k in ['image']:
                data = v[0]
                content_type = v[1]
                filename = u'image.%s' % (content_type.split('/')[1])
                v = NamedBlobImage(data, content_type, filename)
                o.image = v
            if v and getattr(o, k, ''):
                setattr(o, k, v)
        o.exclude_from_nav = True
        o.setEffectiveDate(DateTime())

        wt.doActionFor(o, 'publish')
        o.reindexObject()
        return o

    def processa_feed(self):
        ''' Processa feeds, cria objetos '''
        totais = {'feeds': 0, 'entries': 0}
        totais['feeds'] = 1
        feedName = self.context.Title()
        feedUrl = self.context.remoteUrl
        data = self._getFeed(feedUrl)
        if hasattr(data, 'entries'):
            items = data.entries
            log.info('Feed %s processado: %d items' %
                     (feedName, len(items)))
            itemsDates = []
            for item in items:
                dictNews = self._feedItemsToNews(item,
                                                 feedName)
                if not dictNews:
                    # Already processed
                    log.info('     - Item ja processado')
                    continue
                date = DateTime(dictNews['creation_date'])
                totais['entries'] = totais['entries'] + 1
                itemsDates.append(date)
                self.create_entry(self.context, dictNews)

            if itemsDates:
                # Registra nova data
                itemsDates.sort()
        return totais
