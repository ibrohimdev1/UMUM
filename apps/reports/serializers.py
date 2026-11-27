from rest_framework import serializers
from apps.reports.models import Report

class ReportCreateSerializer(serializers.ModelSerializer):
    listing_id = serializers.IntegerField(required=False, allow_null=True)
    reported_user_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Report
        fields = ['listing_id', 'reported_user_id', 'reason', 'description']
