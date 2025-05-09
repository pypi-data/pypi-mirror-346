"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: __init__.py

brief:
This file defines the configuration for the NetBox plugin named "Interface Relationship Manager".
The plugin is designed to manage relationships between main, receive (rx), 
and transmit (tx) interfaces.
"""
from netbox.plugins import PluginConfig

class InterfaceRelationshipManagerConfig(PluginConfig):
    """
    Plugin configuration class for Interface Relationship Manager.
    """
    name = "interface_relationship_manager"
    verbose_name = "Interface Relationship Manager"
    description = "Manages relationships between main, rx, and tx interfaces"
    version = "1.0.0"
    base_url = "interface_relationship_manager"
    min_version = "3.5.0"

config = InterfaceRelationshipManagerConfig
