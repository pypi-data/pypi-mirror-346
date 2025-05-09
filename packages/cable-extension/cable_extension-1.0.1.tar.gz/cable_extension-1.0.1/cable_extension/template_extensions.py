"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: template_extensions.py

brief:
Provides a sidebar panel on the *Cable* detail page in NetBox that
    shows the extra metadata stored in :class:`~cable_extension.models.CableExtension`.

    The class ``CableExtensionTemplateExtension`` subclasses
    :class:`netbox.plugins.PluginTemplateExtension` and is registered for
    the model label ``dcim.cable``.  When rendering the object view
    NetBox calls ``right_page()``, which injects the template
    ``cable_extension/cable_extension_panel.html`` into the right-hand
    column—but only if the current ``Cable`` instance has an attached
    ``extension`` object.  If no extension exists, no panel is shown.
    
    NOTE: This does not work!!!!!!
"""

from netbox.plugins import PluginTemplateExtension

class CableExtensionTemplateExtension(PluginTemplateExtension):
    models = ['dcim.cable']

    def right_page(self):
        cable = self.context['object']
        extension = getattr(cable, 'extension', None)
        if not extension:
            return ""

        return self.render('cable_extension/cable_extension_panel.html', {
            'extension': extension
        })

template_extensions = [CableExtensionTemplateExtension]
