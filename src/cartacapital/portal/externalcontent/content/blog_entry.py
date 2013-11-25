    # -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone.dexterity.content import Item
from zope.interface import implements
from zope.interface import Interface


def has_image(blog_entry):
    image = blog_entry.image
    return (image and image.getSize())


class IExternalBlogEntry(Interface):
    """
    """


class ExternalBlogEntry(Item):
    implements(IExternalBlogEntry)

    def image_thumb(self):
        ''' Return a thumbnail '''
        if not has_image(self):
            return None
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='image',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        ''' Return a tag to the image '''
        if not (has_image(self)):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image',
                        scale=scale,
                        css_class=css_class,
                        **kw)

    @property
    def section(self):
        blog = aq_parent(self)
        return blog.section
