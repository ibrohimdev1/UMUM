from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from apps.moderation.services.moderation_service import ModerationService
from apps.listings.serializers import ListingListSerializer, ListingDetailSerializer

class ModerationListingListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending = ModerationService.get_pending_listings()
        return Response(ListingListSerializer(pending, many=True).data)

class ModerationListingActionAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        action = request.data.get('action') # 'approve' or 'reject'
        reason = request.data.get('reason', '')

        if action == 'approve':
            listing = ModerationService.approve(pk, request.user)
            return Response(ListingDetailSerializer(listing).data)
        elif action == 'reject':
            if not reason:
                return Response({'error': 'Rad etish sababi ko‘rsatilishi shart'}, status=status.HTTP_400_BAD_REQUEST)
            listing = ModerationService.reject(pk, reason, request.user)
            return Response(ListingDetailSerializer(listing).data)

        return Response({'error': 'Yaroqsiz amal (approve yoki reject kutilmoqda)'}, status=status.HTTP_400_BAD_REQUEST)
