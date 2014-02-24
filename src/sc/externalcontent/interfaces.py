# -*- coding: utf-8 -*-

from sc.externalcontent import _
from zope.interface import Interface
from zope.schema import List, TextLine


class IExternalContentLayer(Interface):
    """ A layer specific for this add-on product.
    """


class ISCExternalContentSettings(Interface):
    """ schema for configlet form """

    rss_sources = List(
        title=_(u'RSS sources'),
        description=_(u'Specify RSS sources, '
                      'one per line. '
                      'The required format is name,url,category.'),
        value_type=TextLine(),
        default=[],
        required=False,
    )
