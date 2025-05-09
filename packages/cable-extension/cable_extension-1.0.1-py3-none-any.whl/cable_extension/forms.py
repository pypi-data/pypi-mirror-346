"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: forms.py

brief:
Contains a form (CableCreateForm) to handle the creation and extension of cables
in NetBox. The form captures necessary cable details, interfaces, and optionally
creates corresponding InventoryItems for both ends of the cable.
"""

from django import forms
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from dcim.models import Cable, Interface, InventoryItem
from dcim.choices import CableTypeChoices, CableLengthUnitChoices

from .models import CableExtension

class CableCreateForm(forms.Form):
    """
    A custom form for creating a Cable object between one or two Interfaces, 
    capturing optional extra fields like serial number, part ID, and more.
    Also supports creating InventoryItems for each end of the cable and 
    storing extended details in a CableExtension record.

    Fields:
        - interface_a, interface_b: The interfaces to be connected by the new cable.
        - cable_serial, cable_part_id: Identifiers for the cable (internal or external).
        - cable_label, cable_type, cable_description: General cable info (label, type, notes).
        - cable_length, cable_length_unit: Physical length of the cable and its unit.
        - create_inventory_for_both_ends: Indicates whether to create an InventoryItem on both devices.
        - manufacturer, comments: Used by CableExtension for extended cable details.

    Validation:
        - Ensures that interface_a and interface_b are not already connected to a cable.

    Save Logic:
        1. Create the Cable object in NetBox with the given info.
        2. Link it to interface_a and optionally interface_b via CableTerminations.
        3. Create one or two InventoryItems if requested.
        4. Store extended cable details (manufacturer, comments) in CableExtension.
    """

    interface_a = forms.ModelChoiceField(
        queryset=Interface.objects.all(),
        label="Interface A",
    )
    interface_b = forms.ModelChoiceField(
        queryset=Interface.objects.all(),
        label="Interface B",
        required=False
    )

    cable_serial = forms.CharField(
        label="Cable Serial Number",
        max_length=100,
        required=False
    )
    cable_part_id = forms.CharField(
        label="Part ID (Cable)",
        max_length=50,
        required=False,
        help_text="Optional internal part code"
    )

    cable_label = forms.CharField(
        label="Cable Label",
        max_length=100,
        required=False
    )
    cable_type = forms.ChoiceField(
        label="Cable Type",
        required=False,
        choices=CableTypeChoices
    )
    cable_description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        required=False
    )
    cable_length = forms.DecimalField(
        label="Length",
        required=False,
        min_value=0
    )
    cable_length_unit = forms.ChoiceField(
        label="Length Unit",
        required=False,
        choices=CableLengthUnitChoices,
        initial=CableLengthUnitChoices.UNIT_METER
    )

    create_inventory_for_both_ends = forms.BooleanField(
        label="Create InventoryItem for both ends?",
        required=False,
        initial=True
    )

    def clean(self):
        """
        Checks that neither interface A nor interface B is already connected 
        to a cable. If they are, adds an error to the form.
        """
        cleaned_data = super().clean()
        int_a = cleaned_data.get('interface_a')
        int_b = cleaned_data.get('interface_b')

        if int_a and int_a.cable:
            self.add_error('interface_a', "Interface A is already connected to a cable!")

        if int_b and int_b.cable:
            self.add_error('interface_b', "Interface B is already connected to a cable!")

        return cleaned_data

    @transaction.atomic
    def save(self):
        """
        Creates the cable, links it to interfaces A (and B if provided),
        optionally creates InventoryItems for each end, and saves 
        extended details in a CableExtension entry.

        Returns:
            The created Cable object.

        Steps:
            1. Create a new Cable using the provided fields (label, type, description, etc.).
            2. Link interface A and possibly B to the Cable via CableTerminations.
            3. If requested, create matching InventoryItems for both ends.
            4. Create a CableExtension record, adding manufacturer and comments data.
        """
        int_a = self.cleaned_data['interface_a']
        int_b = self.cleaned_data['interface_b']

        cable_label = self.cleaned_data.get('cable_label') or ""
        cable_type = self.cleaned_data.get('cable_type')
        cable_description = self.cleaned_data.get('cable_description') or ""
        cable_length = self.cleaned_data.get('cable_length') or 0
        cable_length_unit = self.cleaned_data.get('cable_length_unit') or CableLengthUnitChoices.UNIT_METERS

        cable_serial = self.cleaned_data.get('cable_serial') or ""
        cable_part_id = self.cleaned_data.get('cable_part_id') or ""

        # Create the Cable object
        cable = Cable(
            label=cable_label,
            type=cable_type,
            description=cable_description,
            length=cable_length,
            length_unit=cable_length_unit,
            status='connected',
        )
        cable.save()

        # Attach the cable ends
        interface_ct = ContentType.objects.get_for_model(Interface)
        cable.terminations.create(
            termination_type=interface_ct,
            termination_id=int_a.pk,
            cable_end='A'
        )
        if int_b is not None:
            cable.terminations.create(
                termination_type=interface_ct,
                termination_id=int_b.pk,
                cable_end='B'
            )

        # Create InventoryItem for A
        device_a = int_a.device
        if int_b:
            inv_a = InventoryItem(
                device=device_a,
                name=f"Cable to {int_b.device.name} - {int_b.name}",
                serial=cable_serial,
                part_id=cable_part_id
            )
        else:
            inv_a = InventoryItem(
                device=device_a,
                name="Cable in the air",
                serial=cable_serial,
                part_id=cable_part_id
            )
        inv_a.save()

        # Optionally create InventoryItem for B
        if self.cleaned_data['create_inventory_for_both_ends']:
            if int_b is not None:
                device_b = int_b.device
                inv_b = InventoryItem(
                    device=device_b,
                    name=f"Cable to {device_a.name} - {int_a.name}",
                    serial=cable_serial,
                    part_id=cable_part_id
                )
                inv_b.save()

        # Create or store extended cable details
        manufacturer = self.cleaned_data.get('manufacturer') or ""
        comments = self.cleaned_data.get('comments') or ""
        CableExtension.objects.create(
            cable=cable,
            manufacturer=manufacturer,
            comments=comments
        )

        return cable
