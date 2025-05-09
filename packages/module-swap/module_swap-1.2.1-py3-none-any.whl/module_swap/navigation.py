"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: navigation.py

brief:
This file defines links in the plugin section for easy access to the plugin functions.
"""
from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:module_swap:step1_select',
        link_text='Module Swap',
    ),
    PluginMenuItem(
        link='plugins:module_swap:link_module_inventory_list',
        link_text='Inventory item and module links',
    ),
)
