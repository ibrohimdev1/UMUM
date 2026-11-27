from apps.payments.models import Payment

class PaymentRepository:
    @staticmethod
    def create_payment(order, amount, payme_ref=None, status=Payment.Status.CREATED):
        return Payment.objects.create(
            order=order,
            amount=amount,
            payme_ref=payme_ref,
            status=status
        )

    @staticmethod
    def get_by_payme_ref(payme_ref):
        return Payment.objects.select_related('order', 'order__listing', 'order__buyer').filter(payme_ref=payme_ref).first()

    @staticmethod
    def get_by_order(order):
        return Payment.objects.filter(order=order).first()
