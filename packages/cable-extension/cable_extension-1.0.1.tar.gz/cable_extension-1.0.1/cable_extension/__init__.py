"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: _init__.py

brief:
Defines the configuration for the "Cable Extension" plugin, which augments NetBox
cable data and integrates with an inventory system.
"""

from netbox.plugins import PluginConfig

class CableExtensionConfig(PluginConfig):
    """
    Configuration class for the "Cable Extension" plugin.

    This plugin extends cable-related data within NetBox, offering integration
    with inventory records. It sets the plugin's metadata (name, version, author)
    and establishes a base URL for accessing any plugin-specific views or APIs.
    """

    name = "cable_extension"
    verbose_name = "Cable Extension"
    description = "Plugin for extending cable data and integrating with inventory."
    version = "1.0"
    author = "Viktor Kubec"
    author_email = "Viktor.Kubec@gmail.com"
    base_url = "cable-extension"

config = CableExtensionConfig
