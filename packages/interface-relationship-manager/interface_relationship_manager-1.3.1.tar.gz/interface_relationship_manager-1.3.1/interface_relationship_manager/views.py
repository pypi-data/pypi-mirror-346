"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: views.py

brief:
This module provides a Django view to handle selecting a device and interface
for splitting into separate RX and TX interfaces, utilizing the split_interface utility.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from dcim.models import Device, Interface
from .models import InterfaceRelationship
from .utils import split_interface

def select_device_for_split(request):
    """
    Handles the selection of a device and an interface for splitting. If both are chosen,
    calls the split_interface utility to perform the split. If no device or an invalid
    interface is selected, displays an appropriate error message.

    Args:
        request (HttpRequest): The request object containing user and session data.

    Returns:
        HttpResponse: The rendered template for selecting a device and interface or a
        redirect to the same page upon successful split or when errors occur.
    """
    # Fetch and order all devices
    devices = Device.objects.all().order_by("name")

    selected_device = None
    interfaces = []

    if request.method == "POST":
        device_id = request.POST.get("device")
        interface_id = request.POST.get("interface")

        # If a device is specified, retrieve it and filter interfaces
        if device_id:
            selected_device = get_object_or_404(Device, pk=device_id)
            interfaces = Interface.objects.filter(device=selected_device)

            # Collect IDs of already split interfaces to exclude them
            excluded_interfaces_ids = set()
            for irel in InterfaceRelationship.objects.all():
                excluded_interfaces_ids.add(irel.main_interface_id)
                excluded_interfaces_ids.add(irel.rx_interface_id)
                excluded_interfaces_ids.add(irel.tx_interface_id)

            # Exclude any interfaces involved in existing splits
            interfaces = interfaces.exclude(id__in=excluded_interfaces_ids).order_by("name")

            # If an interface was selected, attempt the split
            if interface_id:
                interface_obj = interfaces.filter(pk=interface_id).first()
                if not interface_obj:
                    messages.error(request, "The selected interface does not exist or has already been split.")
                    return redirect(reverse("plugins:interface_relationship_manager:select_device"))

                try:
                    split_interface(selected_device.id, interface_obj.name)
                    messages.success(
                        request,
                        f"Successfully split interface '{interface_obj.name}' for device '{selected_device.name}'."
                    )
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")

                return redirect(reverse("plugins:interface_relationship_manager:select_device"))

        else:
            messages.error(request, "No device selected.")
            return redirect(reverse("plugins:interface_relationship_manager:select_device"))

    else:
        # Handle GET requests
        device_id = request.GET.get("device")
        if device_id:
            selected_device = get_object_or_404(Device, pk=device_id)
            interfaces = Interface.objects.filter(device=selected_device)

            # Collect IDs of already split interfaces to exclude them
            excluded_interfaces_ids = set()
            for irel in InterfaceRelationship.objects.all():
                excluded_interfaces_ids.add(irel.main_interface_id)
                excluded_interfaces_ids.add(irel.rx_interface_id)
                excluded_interfaces_ids.add(irel.tx_interface_id)

            # Exclude any interfaces involved in existing splits
            interfaces = interfaces.exclude(id__in=excluded_interfaces_ids).order_by("name")

    # Render the template with the relevant devices and interfaces
    return render(
        request,
        "interface_relationship_manager/select_device.html",
        {
            "devices": devices,
            "selected_device": selected_device,
            "interfaces": interfaces,
        }
    )
