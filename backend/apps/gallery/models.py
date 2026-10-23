from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=100)
    # URL-friendly identifier, e.g. "japan-trip" (used in /photos/japan-trip)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    # Lower number = displayed first
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    collections = models.ManyToManyField(
        Collection,
        related_name="photos",
        blank=True,
    )

    # Paths relative to MEDIA_ROOT. They will be filled by the image
    # service in step 3, never typed by hand.
    original_path = models.CharField(max_length=255, blank=True)
    thumb_path = models.CharField(max_length=255, blank=True)
    medium_path = models.CharField(max_length=255, blank=True)
    # Dimensions of the medium version (avoids layout jumps on the front)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title