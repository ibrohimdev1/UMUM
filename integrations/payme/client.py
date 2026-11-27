"""
Payme Merchant API (JSON-RPC 2.0) Integration
Implements standard merchant protocol methods:
- CheckPerformTransaction
- CreateTransaction
- PerformTransaction
- CancelTransaction
- CheckTransaction
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PaymeError:
    TRANSPORT_ERROR = -32300
    ACCESS_DENIED = -32504
    JSON_PARSING_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32400

    # Business specific Payme codes
    ORDER_NOT_FOUND = -31050
    INVALID_AMOUNT = -31001
    TRANSACTION_NOT_FOUND = -31003
    UNABLE_TO_CANCEL = -31007
    UNABLE_TO_PERFORM = -31008

class PaymeIntegration:
    @staticmethod
    def format_error(code, message_uz, message_ru=None, message_en=None, error_id=None):
        return {
            'error': {
                'code': code,
                'message': {
                    'uz': message_uz,
                    'ru': message_ru or message_uz,
                    'en': message_en or message_uz,
                }
            },
            'id': error_id
        }

    @staticmethod
    def format_response(result, req_id):
        return {
            'result': result,
            'id': req_id
        }
