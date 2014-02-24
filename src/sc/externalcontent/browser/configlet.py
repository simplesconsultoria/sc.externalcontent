from plone.app.registry.browser import controlpanel
from sc.externalcontent import _
from sc.externalcontent.interfaces import ISCExternalContentSettings


class ControlPanelForm(controlpanel.RegistryEditForm):

    schema = ISCExternalContentSettings

    label = _('SC external content settings')
    description = _('Settings to configure the import of external content into Plone.')
    form_name = _('SC external content')


class ControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ControlPanelForm
