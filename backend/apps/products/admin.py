"""Products application admin."""

from django.contrib import admin

from .models import Product, ProductSettings


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin view for Product."""

    list_display = (
        "name",
        "price",
        "stock",
        "is_image_uploaded",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    list_filter = ("is_image_uploaded", "created_at", "updated_at")
    list_editable = ("price", "stock")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(ProductSettings)
class ProductSettingsAdmin(admin.ModelAdmin):
    """Admin for singleton ProductSettings."""

    list_display = ("quota", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        """Disable adding new settings if one already exists."""
        if ProductSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """Disable delete to enforce singleton behavior."""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow editing the only instance."""
        return True
