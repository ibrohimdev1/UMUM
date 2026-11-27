from rest_framework import serializers

class AIImproveDescriptionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    raw_description = serializers.CharField(required=False, allow_blank=True, default='')
    category_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

class AISuggestPriceSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    category_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

class AISearchAssistSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200, required=True)
