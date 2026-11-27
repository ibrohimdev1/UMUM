import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.payments.services.payment_service import PaymentService
from integrations.payme.client import PaymeError

class PaymeWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = request.data
            method = data.get('method')
            params = data.get('params', {})
            req_id = data.get('id')

            if not method:
                return Response({'error': {'code': PaymeError.INVALID_REQUEST, 'message': 'Invalid Request'}, 'id': req_id})

            result = PaymentService.handle_payme_rpc(method, params, req_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': {'code': PaymeError.INTERNAL_ERROR, 'message': str(e)}, 'id': request.data.get('id')})
