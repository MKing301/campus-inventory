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

    def __str__(self):
        return self.last_name + ', ' + self.first_name


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
        return self.name


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


class Assignee(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Assignees"

    def __str__(self):
        return self.name


class ItemStatus(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Item_Status"

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    stat = models.ForeignKey(
        ItemStatus,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=250)
    item_location = models.ForeignKey(
        MapLocation,
        on_delete=models.CASCADE
    )
    item_area = models.ForeignKey(
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
    total_cost = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    assigned_to = models.ForeignKey(
        Assignee,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    approved_by = models.ForeignKey(
        ApprovalList,
        on_delete=models.CASCADE
    )
    approved_date = models.DateField()
    purchase_date = models.DateField()
    inserted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    inserted_date = models.DateField()
    modified_by = models.CharField(max_length=150, blank=True, null=True)
    modified_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Inventory_Items"

    def __str__(self):
        return self.name


class ItemNotes(models.Model):
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    inserted_by = models.CharField(max_length=250)
    inserted_date = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name_plural = "Item_Notes"

    def __str__(self):
        return self.item.name
