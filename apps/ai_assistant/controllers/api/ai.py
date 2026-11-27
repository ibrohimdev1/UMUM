from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.ai_assistant.serializers import (
    AIImproveDescriptionSerializer,
    AISuggestPriceSerializer,
    AISearchAssistSerializer
)
from apps.ai_assistant.services.ai_service import AIService

class AIImproveDescriptionAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AIImproveDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = AIService.improve_description(
            title=serializer.validated_data['title'],
            raw_description=serializer.validated_data.get('raw_description', ''),
            category_name=serializer.validated_data.get('category_name', '')
        )
        return Response({'improved_description': res}, status=status.HTTP_200_OK)

class AISuggestPriceAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AISuggestPriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = AIService.suggest_price(
            title=serializer.validated_data['title'],
            category_name=serializer.validated_data.get('category_name', '')
        )
        return Response(res, status=status.HTTP_200_OK)

class AISearchAssistAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = AISearchAssistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = AIService.search_assist(serializer.validated_data['query'])
        return Response(res, status=status.HTTP_200_OK)

class AIChatAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'Xabar kiritilmadi'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = (
            f"Sen UMUM marketplace platformasining rasmiy do‘stona sun‘iy intellekt maslahatchisisan.\n"
            f"Foydalanuvchi senga quyidagi savol yoki murojaatni yo‘lladi:\n"
            f"'{message}'\n\n"
            f"Talablar:\n"
            f"- O‘zbek tilida aniq, foydali, samimiy va chiroyli javob ber;\n"
            f"- Emojilardan o‘rinli foydalan;\n"
            f"- Agar narx yoki tavsiya so‘ragan bo‘lsa, O‘zbekiston bozori bo‘yicha maslahat ber."
        )
        reply = AIService.call_gemini(prompt)
        if not reply:
            reply = "Assalomu alaykum! Men UMUM platformasining aqlli AI yordamchisiman. Sizga qanday yordam bera olaman?"
        return Response({'reply': reply}, status=status.HTTP_200_OK)
