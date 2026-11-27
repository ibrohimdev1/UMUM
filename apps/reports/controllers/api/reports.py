from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.reports.serializers import ReportCreateSerializer
from apps.reports.services.report_service import ReportService

class ReportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            report = ReportService.submit_report(
                user=request.user,
                reason=serializer.validated_data['reason'],
                description=serializer.validated_data.get('description', ''),
                listing_id=serializer.validated_data.get('listing_id'),
                reported_user_id=serializer.validated_data.get('reported_user_id')
            )
            return Response({'id': report.id, 'message': 'Shikoyat administratorga yuborildi.'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)
