from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from .managers import ActiveManager
from django.utils.crypto import get_random_string


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, help_text="Is this category active?")
    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["name"]
        # verbose_name = ("Category")
        # verbose_name_plural = ("Categories")
        indexes = [models.Index(fields=["name", "is_active"])]

    def delete(self, *args, **kwargs):
        self.is_active == False
        self.save()

    def __str__(self):
        return self.name


class InventoryItem(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(
        unique=True,
        max_length=100,
    )
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    reorder_level = models.PositiveIntegerField(
        default=10, help_text="min quantity before reorder alert"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, help_text="Is this item active?")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="inventory_items"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_items",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_items",
    )

    class Meta:
        ordering = ["-created_at"]
        # verbose_name = ("Inventory Item")
        # verbose_name_plural = ("Inventory Items")
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_active", "name"]),
            models.Index(fields=["is_active", "quantity"]),
            models.Index(fields=["is_active", "category"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=0),
                name="quantity_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0), name="price_non_negative"
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{get_random_string(4)}"
        super().save(*args, **kwargs)

    @property
    def is_low_stock(self):
        """check if the stock low or not"""
        return self.quantity <= self.reorder_level

    @property
    def is_empty_stock(self):
        """check if the stock is empty"""
        return self.quantity == 0

    @property
    def total_value(self):
        return self.quantity * self.unit_price
