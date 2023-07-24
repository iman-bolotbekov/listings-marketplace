import json
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Listing, ListingImages, Geolocation
from .serializers import ListingSerializer, ListingImagesSerializer, GeolocationSerializer


@api_view(['GET'])
def getListings(request):
    type_filter = request.GET.get('type')
    offer_filter = request.GET.get('offer')

    listings = Listing.objects.all()

    is_offer = offer_filter == 'offer'
    print(is_offer)

    if type_filter:
        listings = listings.filter(Q(type__iexact=type_filter))

    if offer_filter:
         listings = listings.filter(offer=is_offer)
         print(listings)

    paginator = PageNumberPagination()
    paginator.page_size = 2

    paginated_listings = paginator.paginate_queryset(listings, request)

    serializer = ListingSerializer(paginated_listings, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def getListing(request, pk):
    listings = Listing.objects.get(id=pk)
    serializer = ListingSerializer(listings, many=False, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserListings(request):
    user = request.user
    listings = Listing.objects.filter(userRef=user)
    paginator = PageNumberPagination()
    paginator.page_size = 2

    paginated_listings = paginator.paginate_queryset(listings, request)

    serializer = ListingSerializer(paginated_listings, many=True, context={'request': request})

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createListing(request):
    data = request.data
    user = request.user

    parking = data['parking'] == 'true'
    furnished = data['furnished'] == 'true'
    offer = data['offer'] == 'offer'

    listing = Listing.objects.create(
        name=data['name'],
        type=data['type'],
        userRef=user,
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        parking=parking,
        furnished=furnished,
        offer=offer,
        regularPrice=data['regularPrice'],
        discountedPrice=data['discountedPrice'],
        location=data['location'],
    )

    if 'geolocation' in data:
            geolocation_data = json.loads(data['geolocation'])
            geolocation = Geolocation.objects.create(
                lat=str(geolocation_data['lat']),
                lng=str(geolocation_data['lng'])
            )
            listing.geolocation = geolocation
            listing.save()

    image_set = request.FILES
    if image_set:
        for image_data in image_set.getlist('image'):
                ListingImages.objects.create(listing=listing, image=image_data)

    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateListing(request, pk):
    data = request.data
    listing = Listing.objects.get(id=pk)

    parking = data['parking'] == 'true'
    furnished = data['furnished'] == 'true'
    offer = data['offer'] == 'offer'

    listing.name=data['name']
    listing.type=data['type']
    listing.bedrooms=data['bedrooms']
    listing.bathrooms=data['bathrooms']
    listing.parking=parking
    listing.furnished=furnished
    listing.offer=offer
    listing.regularPrice=data['regularPrice']
    listing.discountedPrice=data['discountedPrice']
    listing.location=data['location']

    image_set = request.FILES
    if image_set:
        previous_images = listing.listingimages_set.all()
        for previous_image in previous_images:
            default_storage.delete(previous_image.image.path)
            previous_image.delete()
        for image_data in image_set.getlist('image'):
                ListingImages.objects.create(listing=listing, image=image_data)

    listing.save()
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteListing(request, pk):
    listing = Listing.objects.get(id=pk)
    listing.delete()
    return Response('Listing was deleted!')