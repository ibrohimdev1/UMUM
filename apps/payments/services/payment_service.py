import time
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.payments.models import Payment
from apps.orders.models import Order
from apps.payments.repositories.payment_repository import PaymentRepository
from apps.orders.repositories.order_repository import OrderRepository
from integrations.payme.client import PaymeError
from integrations.sms.provider import SMSProvider

class PaymentService:
    @classmethod
    def handle_payme_rpc(cls, method, params, req_id):
        """
        Dispatches Payme JSON-RPC methods.
        """
        methods = {
            'CheckPerformTransaction': cls.check_perform_transaction,
            'CreateTransaction': cls.create_transaction,
            'PerformTransaction': cls.perform_transaction,
            'CancelTransaction': cls.cancel_transaction,
            'CheckTransaction': cls.check_transaction,
        }

        handler = methods.get(method)
        if not handler:
            return {'error': {'code': PaymeError.METHOD_NOT_FOUND, 'message': 'Method not found'}, 'id': req_id}

        return handler(params, req_id)

    @classmethod
    def check_perform_transaction(cls, params, req_id):
        account = params.get('account', {})
        order_id = account.get('order_id')
        amount_tiyin = params.get('amount')

        if not order_id:
            return {'error': {'code': PaymeError.ORDER_NOT_FOUND, 'message': {'uz': 'Buyurtma topilmadi'}}, 'id': req_id}

        order = OrderRepository.get_by_id(order_id)
        if not order or order.status != Order.Status.PENDING:
            return {'error': {'code': PaymeError.ORDER_NOT_FOUND, 'message': {'uz': 'Buyurtma mavjud emas yoki to‘langan'}}, 'id': req_id}

        expected_tiyin = int(order.amount * 100)
        if amount_tiyin != expected_tiyin:
            return {'error': {'code': PaymeError.INVALID_AMOUNT, 'message': {'uz': 'Noto‘g‘ri summa'}}, 'id': req_id}

        return {
            'result': {
                'allow': True,
                'detail': {
                    'receipt_type': 0,
                    'items': [{
                        'title': order.listing.title,
                        'price': expected_tiyin,
                        'count': 1,
                        'code': '10101001001000000',
                        'package_code': '123456',
                        'vat_percent': 0
                    }]
                }
            },
            'id': req_id
        }

    @classmethod
    def create_transaction(cls, params, req_id):
        payme_ref = params.get('id')
        account = params.get('account', {})
        order_id = account.get('order_id')
        amount_tiyin = params.get('amount')

        with transaction.atomic():
            payment = PaymentRepository.get_by_payme_ref(payme_ref)
            if payment:
                return {
                    'result': {
                        'create_time': int(payment.created_at.timestamp() * 1000),
                        'transaction': str(payment.id),
                        'state': 1 if payment.status == Payment.Status.CREATED else 2
                    },
                    'id': req_id
                }

            order = OrderRepository.get_by_id(order_id)
            if not order:
                return {'error': {'code': PaymeError.ORDER_NOT_FOUND, 'message': {'uz': 'Buyurtma topilmadi'}}, 'id': req_id}

            amount_sum = Decimal(amount_tiyin) / 100
            payment = PaymentRepository.create_payment(
                order=order,
                amount=amount_sum,
                payme_ref=payme_ref,
                status=Payment.Status.CREATED
            )

            return {
                'result': {
                    'create_time': int(payment.created_at.timestamp() * 1000),
                    'transaction': str(payment.id),
                    'state': 1
                },
                'id': req_id
            }

    @classmethod
    def perform_transaction(cls, params, req_id):
        payme_ref = params.get('id')

        with transaction.atomic():
            payment = PaymentRepository.get_by_payme_ref(payme_ref)
            if not payment:
                return {'error': {'code': PaymeError.TRANSACTION_NOT_FOUND, 'message': {'uz': 'Tranzaksiya topilmadi'}}, 'id': req_id}

            if payment.status == Payment.Status.PERFORMED:
                return {
                    'result': {
                        'transaction': str(payment.id),
                        'perform_time': int(payment.performed_at.timestamp() * 1000),
                        'state': 2
                    },
                    'id': req_id
                }

            payment.status = Payment.Status.PERFORMED
            payment.performed_at = timezone.now()
            payment.save(update_fields=['status', 'performed_at'])

            # Update Order status to PAID
            order = payment.order
            order.status = Order.Status.PAID
            order.save(update_fields=['status', 'updated_at'])

            # Send SMS Notification (FR-13)
            SMSProvider.send_sms(
                order.buyer.phone,
                f"UMUM: #{order.id} buyurtmangiz uchun {order.amount} so‘m to‘lov muvaffaqiyatli qabul qilindi!"
            )

            return {
                'result': {
                    'transaction': str(payment.id),
                    'perform_time': int(payment.performed_at.timestamp() * 1000),
                    'state': 2
                },
                'id': req_id
            }

    @classmethod
    def cancel_transaction(cls, params, req_id):
        payme_ref = params.get('id')
        reason = params.get('reason')

        with transaction.atomic():
            payment = PaymentRepository.get_by_payme_ref(payme_ref)
            if not payment:
                return {'error': {'code': PaymeError.TRANSACTION_NOT_FOUND, 'message': {'uz': 'Tranzaksiya topilmadi'}}, 'id': req_id}

            payment.status = Payment.Status.CANCELLED
            payment.cancel_reason = reason
            payment.save(update_fields=['status', 'cancel_reason'])

            payment.order.status = Order.Status.CANCELLED
            payment.order.save(update_fields=['status'])

            return {
                'result': {
                    'transaction': str(payment.id),
                    'cancel_time': int(timezone.now().timestamp() * 1000),
                    'state': -1 if payment.performed_at is None else -2
                },
                'id': req_id
            }

    @classmethod
    def check_transaction(cls, params, req_id):
        payme_ref = params.get('id')
        payment = PaymentRepository.get_by_payme_ref(payme_ref)
        if not payment:
            return {'error': {'code': PaymeError.TRANSACTION_NOT_FOUND, 'message': {'uz': 'Tranzaksiya topilmadi'}}, 'id': req_id}

        state_map = {
            Payment.Status.CREATED: 1,
            Payment.Status.PERFORMED: 2,
            Payment.Status.CANCELLED: -1 if payment.performed_at is None else -2,
            Payment.Status.FAILED: -1
        }

        return {
            'result': {
                'create_time': int(payment.created_at.timestamp() * 1000),
                'perform_time': int(payment.performed_at.timestamp() * 1000) if payment.performed_at else 0,
                'cancel_time': 0,
                'transaction': str(payment.id),
                'state': state_map.get(payment.status, 1),
                'reason': payment.cancel_reason
            },
            'id': req_id
        }
