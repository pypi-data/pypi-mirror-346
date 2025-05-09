"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: models.py

brief:
Model representing a one-to-one relationship between Modules and Inventory Items in NetBox.
This link ensures a clear association and easy tracking between hardware modules 
and their inventory counterparts.
"""
from django.db import models
from dcim.models import Module, InventoryItem


class ModuleInventoryLink(models.Model):
    """
    Database model linking a Module to an InventoryItem with a one-to-one relationship.
    Ensures each module is uniquely associated with one inventory item and vice versa.
    """
    module = models.OneToOneField(
        Module,
        on_delete=models.CASCADE,
        related_name='inventory_link',
        help_text="The module being linked to an inventory item."
    )
    inventory_item = models.OneToOneField(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='module_link',
        help_text="The inventory item corresponding to the module."
    )

    def __str__(self):
        """Human-readable representation of the ModuleInventoryLink object."""
        return f"Module {self.module} <-> InventoryItem {self.inventory_item}"
