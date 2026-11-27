from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from apps.accounts.serializers.user_serializer import UserSerializer, UserProfileUpdateSerializer
from apps.accounts.services.user_service import UserProfileService

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(request=UserProfileUpdateSerializer, responses={200: UserSerializer})
    def put(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = UserProfileService.update_profile(
            request.user,
            **serializer.validated_data
        )
        return Response(UserSerializer(updated_user).data)
