from rest_framework import serializers

from .models import ListingImages, Listing, Geolocation


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = ['id','lat', 'lng']


class ListingImagesSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = ListingImages
        fields = ['imageUrl', 'id']

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ListingSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField(read_only=True)
    geolocation = serializers.SerializerMethodField(read_only=True)

    def get_imageUrls(self, obj):
        images = obj.listingimages_set.all()
        serializer = ListingImagesSerializer(images, many=True, context=self.context)
        return serializer.data

    def get_geolocation(self, obj):
        serializer = GeolocationSerializer(obj.geolocation, many=False)
        return serializer.data

    class Meta:
        model = Listing
        fields = '__all__'