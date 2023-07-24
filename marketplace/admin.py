from django.contrib import admin
from . import models

admin.site.register(models.Listing)
admin.site.register(models.ListingImages)
admin.site.register(models.Geolocation)
