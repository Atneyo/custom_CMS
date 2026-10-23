from django.contrib import admin

from .models import Collection, Photo


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    # Fills the slug automatically while typing the name
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "created_at")
    list_editable = ("order",)
    list_filter = ("collections",)
    search_fields = ("title", "description")
    # Two-column selector, much easier than a multi-select box
    filter_horizontal = ("collections",)