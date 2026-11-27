from rest_framework.views import APIView
from rest_framework.response import Response
from apps.categories.services.category_service import CategoryService
from apps.categories.serializers import CategorySerializer
from drf_spectacular.utils import extend_schema

class CategoryListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request):
        categories = CategoryService.get_category_tree()
        return Response(CategorySerializer(categories, many=True).data)
