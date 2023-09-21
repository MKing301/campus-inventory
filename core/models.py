from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = ('ADMIN', 'Admin')
        LEADER = ('LEADER', 'Leader')
        MEMBER = ('MEMBER', 'Member')
        GUEST = ('GUEST', 'Guest')

    role = models.CharField(
        name='Role',
        max_length=50,
        choices=Role.choices,
        null=True,
        blank=True
    )


class Contact(models.Model):
    fullname = models.CharField(max_length=75)
    contact_email = models.EmailField()
    contact_subject = models.CharField(max_length=50)
    contact_message = models.TextField()
    inserted_date = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name_plural = "Catalog_Contacts"

    def __str__(self):
        return self.fullname


class MapLocation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Map_Locations"

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    map_loc = models.ForeignKey(
        MapLocation,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Areas"

    def __str__(self):
        return self.map_loc.name + ' - ' + self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Manufacturers"

    def __str__(self):
        return self.name


class ApprovalList(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Approval_List"

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    location = models.ForeignKey(
        Area,
        on_delete=models.CASCADE
    )
    mfg = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE
    )
    model_no = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100, blank=True, null=True)
    qty = models.IntegerField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    assigned_to = models.CharField(max_length=150)
    approved_by = models.ForeignKey(
        ApprovalList,
        on_delete=models.CASCADE
    )
    approved_date = models.DateField()
    purchase_date = models.DateField()
    inserted_by = models.CharField(max_length=150)
    inserted_date = models.DateField()
    modified_by = models.CharField(max_length=150)
    modified_date = models.DateField()

    class Meta:
        verbose_name_plural = "Inventory_Items"

    def __str__(self):
        return self.name
