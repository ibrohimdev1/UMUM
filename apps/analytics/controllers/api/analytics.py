from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.accounts.models import User
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.analytics.services.analytics_service import AnalyticsService

class AdminUsersAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        return Response(UserSerializer(users, many=True).data)

class AdminUserDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = User.objects.get(id=pk)
        new_status = request.data.get('status')
        if new_status in User.Status.values:
            user.status = new_status
            user.save(update_fields=['status'])
        return Response(UserSerializer(user).data)

class AdminStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = AnalyticsService.get_system_stats()
        return Response(stats)
