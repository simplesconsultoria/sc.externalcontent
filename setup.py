# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0rc1'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='cartacapital.portal.externalcontent',
      version=version,
      description=u"Integração da Carta Capital com conteúdo externo.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.2',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
          'Topic :: Multimedia',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.cartacapital.com.br',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['cartacapital', 'cartacapital.portal'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.nitf',
          'feedparser',
          'five.grok',
          'Plone',
          'plone.app.dexterity',
          'plone.namedfile [blobs]',
          'Products.CMFCore',
          'Products.CMFPlone >=4.2',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
