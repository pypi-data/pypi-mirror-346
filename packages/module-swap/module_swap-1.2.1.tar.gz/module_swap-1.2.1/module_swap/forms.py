"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: forms.py

brief:
Forms for handling module swaps and linking modules with inventory items in NetBox.
"""
from django import forms
from django.db.models import Exists, OuterRef
from dcim.models import Device, Module, ModuleBay
from .models import ModuleInventoryLink


def get_devices_with_free_bay():
    """
    Retrieves devices that have at least one available (empty) module bay.

    Returns:
        QuerySet: Devices with free module bays.
    """
    # Query to get module bays without modules installed
    free_bays = ModuleBay.objects.filter(
        ~Exists(
            Module.objects.filter(module_bay_id=OuterRef('pk'))
        )
    )
    # Get device IDs that have free module bays
    device_ids = free_bays.values_list('device_id', flat=True).distinct()
    # Return devices filtered by the obtained IDs
    return Device.objects.filter(pk__in=device_ids)


class Step1SelectForm(forms.Form):
    """
    Form for selecting a module to move and choosing the target device.
    """
    selected_module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label="Module to move"
    )
    target_device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label="Target device"
    )

    def __init__(self, *args, module_id=None, **kwargs):
        """
        Initializes the form, optionally pre-selecting a module and limiting the module queryset.

        Args:
            module_id (int, optional): ID of the module to pre-select.
        """
        super().__init__(*args, **kwargs)
        # Limit the target_device queryset to devices with available module bays
        self.fields['target_device'].queryset = get_devices_with_free_bay()

        # If module_id is provided, set the initial selection and limit the queryset
        if module_id:
            try:
                mod = Module.objects.get(pk=module_id)
                self.fields['selected_module'].initial = mod
                self.fields['selected_module'].queryset = Module.objects.filter(pk=module_id)
            except Module.DoesNotExist:
                pass


class Step2BayForm(forms.Form):
    """
    Form for selecting the target module bay on the chosen device.
    """
    target_module_bay = forms.ModelChoiceField(
        queryset=ModuleBay.objects.none(),
        label="Target module bay",
        required=True
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, dynamically setting available module bays based 
        on the selected device.

        Args:
            device_id (int, optional): ID of the device to filter module bays.
        """
        device_id = kwargs.pop('device_id', None)
        super().__init__(*args, **kwargs)

        # Dynamically set module bays available for the given device
        if device_id:
            self.fields['target_module_bay'].queryset = ModuleBay.objects.filter(
                device_id=device_id)


class LinkModuleInventoryForm(forms.ModelForm):
    """
    Form for creating or updating a link between a module and an inventory item.
    Ensures each module and inventory item can only be linked once.
    """

    class Meta:
        model = ModuleInventoryLink
        fields = ['module', 'inventory_item']

    def clean(self):
        """
        Validates uniqueness constraints for module-inventory item links.

        Raises:
            ValidationError: If the module or inventory item is already linked elsewhere.
        """
        cleaned_data = super().clean()
        module = cleaned_data.get('module')
        inventory_item = cleaned_data.get('inventory_item')

        # Check if the module is already linked with another inventory item
        if ModuleInventoryLink.objects.filter(module=module).exclude(pk=self.instance.pk).exists():
            self.add_error('module', 'This module is already linked with another InventoryItem.')

        # Check if the inventory item is already linked with another module
        if ModuleInventoryLink.objects.filter(inventory_item=inventory_item).exclude(
            pk=self.instance.pk).exists():
            self.add_error('inventory_item', 'This InventoryItem is'
                        'already linked with another module.')

        return cleaned_data
