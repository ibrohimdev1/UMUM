from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from apps.accounts.serializers.user_serializer import RequestOTPSerializer, VerifyOTPSerializer, UserSerializer
from apps.accounts.services.auth_service import AuthService

class RequestCodeAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=RequestOTPSerializer, responses={200: dict})
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = AuthService.request_otp(serializer.validated_data['phone'])
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=VerifyOTPSerializer, responses={200: dict})
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = AuthService.verify_otp(
                serializer.validated_data['phone'],
                serializer.validated_data['code']
            )
            return Response({
                'user': UserSerializer(result['user']).data,
                'is_new_user': result['is_new_user'],
                'tokens': result['tokens']
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)
