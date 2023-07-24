from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


TYPE = (
    ('rent', 'rent'),
    ('sale', 'sale'),
)

class Geolocation(models.Model):
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'lat - {self.lat},lng - {self.lng}'


class Listing(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE, db_index=True)
    userRef = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    bedrooms = models.PositiveBigIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking = models.BooleanField(default=False, null=True, blank=True)
    furnished = models.BooleanField(default=False, null=True, blank=True)
    offer = models.BooleanField(default=False, db_index=True, null=True, blank=True)
    regularPrice = models.PositiveIntegerField()
    discountedPrice = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name


class ListingImages(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing/images/')

    def __str__(self) -> str:
        return str(self.image.url)