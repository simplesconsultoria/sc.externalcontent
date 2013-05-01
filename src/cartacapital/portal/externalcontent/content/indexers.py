# -*- coding: utf-8 -*-
from cartacapital.portal.externalcontent.content import blog
from cartacapital.portal.externalcontent.content import blog_entry
from five import grok
from plone.indexer.decorator import indexer


def SearchableText(obj, text=False):
    return u' '.join((obj.id, obj.title, obj.description, ))


@indexer(blog.IExternalBlog)
def SearchableText_blog(obj):
    return SearchableText(obj)

grok.global_adapter(SearchableText_blog,
                    name="SearchableText")


@indexer(blog_entry.IExternalBlogEntry)
def SearchableText_blog_entry(obj):
    if obj.text is None or obj.text.output is None:
        return SearchableText(obj)
    text = u' '.join((SearchableText(obj), obj.text.output.decode('utf-8')))
    return text

grok.global_adapter(SearchableText_blog_entry,
                    name="SearchableText")


@indexer(blog_entry.IExternalBlogEntry)
def getRemoteUrl(obj):
    return obj.remoteUrl

grok.global_adapter(getRemoteUrl,
                    name="SearchableText_blog_entry")
