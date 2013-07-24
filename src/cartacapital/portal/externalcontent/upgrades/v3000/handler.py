# -*- coding:utf-8 -*-
from cartacapital.portal.externalcontent.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging

PROFILE = 'profile-cartacapital.portal.externalcontent.upgrades.v3000:default'


def apply_profile(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    profile = PROFILE
    loadMigrationProfile(context, profile)
    logger.info('Loaded upgrade profile to version 3000')
