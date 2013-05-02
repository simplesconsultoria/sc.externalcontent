# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implements
from zope.interface import Interface


class IExternalBlog(Interface):
    """
    """


class ExternalBlog(Container):
    implements(IExternalBlog)
