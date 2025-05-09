"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: models.py

brief:
This file defines the InterfaceRelationship model used in the Interface Relationship Manager plugin.
The model allows linking one main interface to separate receive (rx) and transmit (tx) interfaces.
"""
from django.db import models
from dcim.models import Interface

class InterfaceRelationship(models.Model):
    """
    A model to define relationships between a main interface and its 
    associated RX and TX interfaces.

    Attributes:
        main_interface (OneToOneField): The primary interface in the relationship.
        rx_interface (OneToOneField): The interface used for receiving data.
        tx_interface (OneToOneField): The interface used for transmitting data.
    """
    main_interface = models.OneToOneField(
        Interface,
        on_delete=models.CASCADE,
        related_name='main_relationship'
    )
    rx_interface = models.OneToOneField(
        Interface,
        on_delete=models.CASCADE,
        related_name='rx_relationship'
    )
    tx_interface = models.OneToOneField(
        Interface,
        on_delete=models.CASCADE,
        related_name='tx_relationship'
    )

    def __str__(self):
        return f"{self.main_interface} -> {self.rx_interface}, {self.tx_interface}"
