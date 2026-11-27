from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from apps.listings.models import Listing
from apps.listings.serializers import (
    ListingListSerializer,
    ListingDetailSerializer,
    ListingCreateSerializer,
    ListingImageSerializer,
    MapListingSerializer
)
from apps.listings.repositories.listing_repository import ListingRepository
from apps.listings.services.listing_service import ListingService

class ListingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(responses={200: ListingListSerializer(many=True)})
    def get(self, request):
        query = request.GET.get('search')
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        city = request.GET.get('city')
        ordering = request.GET.get('ordering', '-created_at')

        listings = ListingRepository.search(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            city=city,
            ordering=ordering
        )
        return Response(ListingListSerializer(listings, many=True).data)

    @extend_schema(request=ListingCreateSerializer, responses={201: ListingDetailSerializer})
    def post(self, request):
        serializer = ListingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            listing = ListingService.create_listing(
                user=request.user,
                **serializer.validated_data
            )
            return Response(ListingDetailSerializer(listing).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)

class ListingDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(responses={200: ListingDetailSerializer})
    def get(self, request, pk):
        listing = ListingRepository.get_by_id(pk)
        if not listing:
            return Response({'error': 'E‘lon topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ListingDetailSerializer(listing).data)

    @extend_schema(request=ListingCreateSerializer, responses={200: ListingDetailSerializer})
    def put(self, request, pk):
        serializer = ListingCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            listing = ListingService.update_listing(request.user, pk, **serializer.validated_data)
            return Response(ListingDetailSerializer(listing).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            ListingService.archive_listing(request.user, pk)
            return Response({'message': 'E‘lon muvaffaqiyatli arxivlandi'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListingMapAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses={200: MapListingSerializer(many=True)})
    def get(self, request):
        listings = ListingRepository.get_map_listings()
        return Response(MapListingSerializer(listings, many=True).data)

class ListingImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        listing = ListingRepository.get_by_id(pk)
        if not listing or listing.user_id != request.user.id:
            return Response({'error': 'Ruxsat berilmagan'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get('image')
        if not file_obj:
            return Response({'error': 'Rasm fayli yuborilmadi'}, status=status.HTTP_400_BAD_REQUEST)

        image_obj = ListingRepository.add_image(listing, image_file=file_obj)
        return Response(ListingImageSerializer(image_obj).data, status=status.HTTP_201_CREATED)
