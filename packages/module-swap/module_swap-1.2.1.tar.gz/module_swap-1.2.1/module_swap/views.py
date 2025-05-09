"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: views.py

brief:
Views for handling module swaps and linking modules with inventory items in NetBox.
This includes a multi-step form for moving modules between devices and managing 
module-inventory item associations.
"""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.views.generic import DeleteView, ListView
from django.urls import reverse_lazy
from .forms import Step1SelectForm, Step2BayForm, LinkModuleInventoryForm
from dcim.models import Module, ModuleBay
from .models import ModuleInventoryLink


class Step1SelectView(View):
    """
    Step 1: Select the module to move and the target device.
    """
    template_name = 'module_swap/step1_select.html'

    def get(self, request):
        """Render form for selecting a module and a target device."""
        module_id = request.GET.get('module_id')
        form = Step1SelectForm(module_id=module_id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Process form submission and store selections in session."""
        form = Step1SelectForm(request.POST)
        if form.is_valid():
            selected_module = form.cleaned_data['selected_module']
            target_device = form.cleaned_data['target_device']
            # Save selected module and target device IDs in session for use in next step
            request.session['selected_module_id'] = selected_module.pk
            request.session['target_device_id'] = target_device.pk
            return redirect('plugins:module_swap:step2_bay')
        messages.error(request, "Invalid module or device selection.")
        return render(request, self.template_name, {'form': form})


class Step2BayView(View):
    """
    Step 2: Select the target module bay within the selected device.
    Handles the actual module transfer within a transaction.
    """
    template_name = 'module_swap/step2_bay.html'

    def get(self, request):
        """Render form for selecting the target module bay."""
        device_id = request.session.get('target_device_id')
        if not device_id:
            messages.warning(request, "First, select a device in step 1.")
            return redirect('plugins:module_swap:step1_select')
        form = Step2BayForm(device_id=device_id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handle the module transfer to the selected module bay."""
        device_id = request.session.get('target_device_id')
        module_id = request.session.get('selected_module_id')
        if not (device_id and module_id):
            messages.warning(request, "You must first select a module and device in step 1.")
            return redirect('plugins:module_swap:step1_select')

        form = Step2BayForm(request.POST, device_id=device_id)
        if form.is_valid():
            target_module_bay = form.cleaned_data['target_module_bay']
            selected_module = Module.objects.get(pk=module_id)

            try:
                with transaction.atomic():
                    # Clear the previous module bay to remove the module association
                    old_bay = ModuleBay.objects.filter(module=selected_module).first()
                    if old_bay:
                        old_bay.module = None
                        old_bay.save()

                    # Assign module to the new bay and update the device
                    selected_module.module_bay = target_module_bay
                    selected_module.device_id = target_module_bay.device_id
                    selected_module.save()

                    # Update linked inventory item's device, if such a link exists
                    try:
                        link = ModuleInventoryLink.objects.get(module=selected_module)
                        inv_item = link.inventory_item
                        inv_item.device_id = target_module_bay.device_id
                        inv_item.save()
                    except ModuleInventoryLink.DoesNotExist:
                        # Ignore if no link exists
                        pass

                messages.success(request, 'Module successfully moved to the new module'
                                'bay (and InventoryItem if applicable).')
                # Clear session variables after successful transfer
                del request.session['target_device_id']
                del request.session['selected_module_id']
                return redirect('dcim:device', pk=target_module_bay.device.pk)
            except Exception as e:
                # Handle unexpected errors gracefully
                messages.error(request, f"Error during transfer: {e}")
        else:
            messages.error(request, "Invalid module bay selection.")
        return render(request, self.template_name, {'form': form})


class LinkModuleInventoryView(View):
    """
    View to create or update a link between modules and inventory items.
    """
    template_name = "module_swap/link_module_inventory.html"

    def get(self, request, link_id=None):
        """Render form for creating or updating a module-inventory link."""
        form = LinkModuleInventoryForm(instance=get_object_or_404(
            ModuleInventoryLink, pk=link_id)) if link_id else LinkModuleInventoryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, link_id=None):
        """Process form submission for creating/updating module-inventory links."""
        instance = get_object_or_404(ModuleInventoryLink, pk=link_id) if link_id else None
        form = LinkModuleInventoryForm(request.POST, instance=instance)

        if form.is_valid():
            link = form.save(commit=False)
            module = link.module
            inventory_item = link.inventory_item

            # Assign inventory item to the module's device to maintain consistency
            if module.device_id:
                inventory_item.device_id = module.device_id
                inventory_item.save()

            link.save()
            return redirect("plugins:module_swap:link_module_inventory_list")
        return render(request, self.template_name, {"form": form})


class LinkModuleInventoryListView(ListView):
    """
    Displays a list of existing module-inventory links.
    """
    model = ModuleInventoryLink
    template_name = "module_swap/link_module_inventory_list.html"
    context_object_name = "links"


class DeleteModuleInventoryLinkView(DeleteView):
    """
    Deletes a module-inventory item link.
    """
    model = ModuleInventoryLink
    template_name = "module_swap/link_module_inventory_confirm_delete.html"
    success_url = reverse_lazy("plugins:module_swap:link_module_inventory_list")
