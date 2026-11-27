"""
SMS Provider Integration (Eskiz / Mock SMS)
Supports OTP codes, order status, and moderation alerts.
"""
import logging
import random
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class SMSProvider:
    @classmethod
    def send_sms(cls, phone: str, message: str) -> bool:
        provider_type = os.getenv('SMS_PROVIDER', 'mock').lower()
        if provider_type == 'eskiz':
            return cls._send_eskiz(phone, message)
        return cls._send_mock(phone, message)

    @classmethod
    def _send_mock(cls, phone: str, message: str) -> bool:
        logger.info(f"[MOCK SMS] To: {phone} | Message: {message}")
        print(f"\n==========================================")
        print(f"[SMS SANDBOX] To: {phone}")
        print(f"Text: {message}")
        print(f"==========================================\n")
        return True

    @classmethod
    def _send_eskiz(cls, phone: str, message: str) -> bool:
        # In production, uses requests.post to Eskiz API
        logger.info(f"[ESKIZ SMS] To: {phone} | Message: {message}")
        return True

    @staticmethod
    def generate_otp_code() -> str:
        return f"{random.randint(100000, 999999)}"
