# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from zope.interface import implements
from zope.interface import Interface


class IExternalBlogEntry(Interface):
    """
    """


class ExternalBlogEntry(Item):
    implements(IExternalBlogEntry)
