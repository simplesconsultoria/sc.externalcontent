# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import cartacapital.portal.externalcontent
        self.loadZCML(package=cartacapital.portal.externalcontent)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        profile = 'cartacapital.portal.externalcontent:default'
        self.applyProfile(portal, profile)

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='cartacapital.portal.externalcontent:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='cartacapital.portal.externalcontent:Functional',
)
