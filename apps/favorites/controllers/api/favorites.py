from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.favorites.services.favorite_service import FavoriteService
from apps.favorites.serializers import FavoriteSerializer

class FavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favs = FavoriteService.get_favorites(request.user)
        return Response(FavoriteSerializer(favs, many=True).data)

    def post(self, request, listing_id):
        res = FavoriteService.toggle(request.user, listing_id)
        return Response(res, status=status.HTTP_200_OK)

    def delete(self, request, listing_id):
        from apps.favorites.repositories.favorite_repository import FavoriteRepository
        FavoriteRepository.remove(request.user, listing_id)
        return Response({'message': 'Sevimlilardan olib tashlandi'}, status=status.HTTP_200_OK)
