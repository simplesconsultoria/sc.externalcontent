.. contents::

Introduction
------------

Integração de conteúdo externo RSS no Plone.

Installation
------------

To enable this package in a buildout-based installation:

1. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        sc.externalcontent

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``sc.externalcontent`` and click the
'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.
