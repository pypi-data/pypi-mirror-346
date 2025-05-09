"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: __init__.py

brief:
Defines the configuration metadata for the Module Swap plugin.
"""
from django.urls import path, include
from netbox.plugins import PluginConfig

class ModuleSwapConfig(PluginConfig):
    """
    Module swap plugin configuration.

    This plugin enables swapping modules between devices in NetBox
    while preserving module history.
    This class defines the plugin configuration by subclassing NetBox's PluginConfig.
    """
    name = 'module_swap'
    verbose_name = 'Module Swap'
    description = 'Plugin allows swapping modules between devices while keeping history.'
    version = '1.0'
    author = 'Viktor Kubec'
    author_email = 'Viktor.Kubec@gmail.com'
    base_url = 'module-swap'

config = ModuleSwapConfig
