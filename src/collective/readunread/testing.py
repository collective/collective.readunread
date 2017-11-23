# -*- coding: utf-8 -*-
# from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

import collective.readunread


class CollectiveReadunreadLayer(PloneSandboxLayer):

    # defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.readunread, name='testing.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.readunread:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        content = api.content.create(container=portal, id='tt1', type='testtype', title='My content')
        content.reindexObject()


COLLECTIVE_READUNREAD_FIXTURE = CollectiveReadunreadLayer()


COLLECTIVE_READUNREAD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_READUNREAD_FIXTURE,),
    name='CollectiveReadunreadLayer:IntegrationTesting'
)


COLLECTIVE_READUNREAD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_READUNREAD_FIXTURE,),
    name='CollectiveReadunreadLayer:FunctionalTesting'
)


COLLECTIVE_READUNREAD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_READUNREAD_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveReadunreadLayer:AcceptanceTesting'
)
