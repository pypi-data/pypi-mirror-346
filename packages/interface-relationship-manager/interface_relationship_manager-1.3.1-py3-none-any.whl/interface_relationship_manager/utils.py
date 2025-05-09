"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: utils.py

brief:
This module provides a utility function for splitting a single network interface
into separate RX and TX interfaces in a NetBox-based environment.
"""

from dcim.models import Device, Interface
from .models import InterfaceRelationship

def split_interface(device_id, interface_name):
    """
    Splits a single interface on the specified device into an RX interface and
    a TX interface. The original interface is retained as the 'main interface'.

    Args:
        device_id (int): Primary key of the device whose interface is being split.
        interface_name (str): Name of the interface to be split.

    Raises:
        ValueError: If the specified interface does not exist or if an error
                    occurs during the split process.

    Returns:
        None
    """
    try:
        # Retrieve the device object by its primary key.
        device = Device.objects.get(pk=device_id)

        # Find the original interface on the device to split.
        original_interface = Interface.objects.filter(device=device, name=interface_name).first()
        if not original_interface:
            raise ValueError(f"Interface '{interface_name}' not found for device {device.name}.")

        # Create the RX interface, using the original interface as the parent.
        rx_interface = Interface.objects.create(
            device=device,
            name=f"{original_interface.name}_rx",
            type=original_interface.type,
            parent=original_interface,
            description=f"RX interface for {original_interface.name}"
        )

        # Create the TX interface, also using the original interface as the parent.
        tx_interface = Interface.objects.create(
            device=device,
            name=f"{original_interface.name}_tx",
            type=original_interface.type,
            parent=original_interface,
            description=f"TX interface for {original_interface.name}"
        )

        # Create a relationship record linking the main (original), RX, and TX interfaces.
        InterfaceRelationship.objects.create(
            main_interface=original_interface,
            rx_interface=rx_interface,
            tx_interface=tx_interface
        )

    except Exception as e:
        raise ValueError(f"An error occurred during interface split: {e}")
