"""
This file defines links in the plugin section for easy access to the plugin functions.
"""
from netbox.plugins import PluginMenuItem

menu_items = [
    PluginMenuItem(
        link='plugins:interface_relationship_manager:select_device',
        link_text='Split Interface',
        permissions=['dcim.change_device']
    )
]
