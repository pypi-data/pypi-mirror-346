"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: views.py

brief:
Contains view classes for handling cable creation and editing cable extension data.
These views integrate custom forms for adding new cables with optional inventory items
and for modifying extended cable information (CableExtension).
"""

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View

from .forms import CableCreateForm, CableCreateForm  # Possibly a typo – check for duplication
from .models import CableExtension

class CableCreateView(View):
    """
    A view to create new cables in NetBox.

    GET: Renders an empty CableCreateForm.
    POST: Validates the form data. If valid, a Cable object (and optional InventoryItems)
        is created, followed by a redirect to the cable's detail page. Otherwise,
        re-renders the form with validation errors.
    """

    template_name = 'cable_extension/cable_create.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests by showing an empty CableCreateForm.
        """
        form = CableCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests by validating form data. Creates the cable and related
        records upon success, then redirects to the NetBox cable detail. If invalid,
        displays form errors.
        """
        form = CableCreateForm(request.POST)
        if form.is_valid():
            cable = form.save()
            messages.success(request, f"Cable (ID={cable.pk}) created successfully!")
            return redirect(reverse('dcim:cable', args=[cable.pk]))
        return render(request, self.template_name, {'form': form})


class CableExtensionEditView(View):
    """
    A view for editing existing CableExtension records linked to cables.

    GET: Renders a form pre-filled with the existing CableExtension data.
    POST: Validates the updated data. If valid, saves changes and redirects to
        the related cable's detail page. Otherwise, re-renders with errors.
    """

    template_name = 'cable_extension/cable_extension_edit.html'

    def get(self, request, pk):
        """
        Load the CableExtension object by primary key, then present a form for editing.
        """
        extension = get_object_or_404(CableExtension, pk=pk)
        form = CableExtensionForm(instance=extension)
        return render(request, self.template_name, {
            'form': form,
            'extension': extension
        })

    def post(self, request, pk):
        """
        Validate the submitted form data against the existing CableExtension instance.
        If valid, saves changes and redirects to the related cable's detail page.
        Otherwise, displays errors.
        """
        extension = get_object_or_404(CableExtension, pk=pk)
        form = CableExtensionForm(request.POST, instance=extension)
        if form.is_valid():
            form.save()
            messages.success(request, "Cable extension updated successfully!")
            return redirect(reverse('dcim:cable', args=[extension.cable.pk]))
        return render(request, self.template_name, {
            'form': form,
            'extension': extension
        })
