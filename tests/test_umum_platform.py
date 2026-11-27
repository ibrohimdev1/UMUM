from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError, PermissionDenied
from apps.accounts.models import User, OTPVerification
from apps.categories.models import Category
from apps.listings.models import Listing
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.accounts.services.auth_service import AuthService
from apps.listings.services.listing_service import ListingService
from apps.payments.services.payment_service import PaymentService
from apps.chats.services.chat_service import ChatService
from apps.ai_assistant.services.ai_service import AIService

class UMUMPlatformTestCase(TestCase):
    def setUp(self):
        # Setup base test data
        self.client = Client()
        self.seller = User.objects.create_user(
            phone='+998901112233',
            full_name='Test Sotuvchi',
            seller_profile_completed=True,
            city='Toshkent'
        )
        self.buyer = User.objects.create_user(
            phone='+998909998877',
            full_name='Test Xaridor',
            city='Samarqand'
        )
        self.category = Category.objects.create(name='Elektronika', icon='fas fa-laptop')
        self.listing = Listing.objects.create(
            user=self.seller,
            category=self.category,
            title='MacBook Pro M3',
            description='Yangi holatda',
            price=20000000,
            status=Listing.Status.ACTIVE
        )

    # TC-01: To‘g‘ri SMS-kod bilan ro‘yxatdan o‘tish
    def test_tc01_valid_sms_registration_and_login(self):
        phone = '+998905554433'
        otp_req = AuthService.request_otp(phone)
        code = otp_req['debug_code']

        verify_res = AuthService.verify_otp(phone, code)
        self.assertIsNotNone(verify_res['user'])
        self.assertEqual(verify_res['user'].phone, phone)
        self.assertTrue('access' in verify_res['tokens'])

    # TC-02: Noto‘g‘ri yoki muddati o‘tgan SMS-kod kiritish
    def test_tc02_invalid_sms_code(self):
        phone = '+998905554433'
        AuthService.request_otp(phone)
        with self.assertRaises(ValidationError):
            AuthService.verify_otp(phone, '000000')

    # TC-03: To‘liq ma’lumot bilan e‘lon qo‘shish (MODERATION holatida bo'lishi)
    def test_tc03_create_listing_success(self):
        new_listing = ListingService.create_listing(
            user=self.seller,
            title='Sony PlayStation 5',
            description='2 ta joystik bilan',
            price=7000000,
            category_id=self.category.id,
            city='Toshkent'
        )
        self.assertEqual(new_listing.status, Listing.Status.MODERATION)
        self.assertEqual(new_listing.user, self.seller)

    # TC-04: Majburiy maydonsiz e‘lon yuborish
    def test_tc04_missing_seller_profile_blocks_listing(self):
        unverified_user = User.objects.create_user(phone='+998971112233', seller_profile_completed=False)
        with self.assertRaises(ValidationError):
            ListingService.create_listing(
                user=unverified_user,
                title='Test Phone',
                description='Desc',
                price=1000000,
                category_id=self.category.id
            )

    # TC-05: Mavjud bo‘lmagan kalit so‘z bilan qidirish
    def test_tc05_empty_search_results(self):
        response = self.client.get(reverse('search') + '?q=mavjud_bolmagan_maxsulot_xyz999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['listings']), 0)

    # TC-06: Chatda xabar yuborish
    def test_tc06_chat_messaging(self):
        chat = ChatService.start_chat(self.buyer, self.listing.id)
        msg = ChatService.send_message(self.buyer, chat.id, "Salom, narxini tushirasizmi?")
        self.assertEqual(msg.body, "Salom, narxini tushirasizmi?")
        self.assertEqual(msg.sender, self.buyer)

    # TC-07: Payme orqali muvaffaqiyatli to‘lov
    def test_tc07_payme_successful_payment(self):
        order = Order.objects.create(listing=self.listing, buyer=self.buyer, amount=self.listing.price)
        req_id = 'test_req_1'
        payme_trans_id = 'payme_mock_999'

        # 1. Check
        res1 = PaymentService.check_perform_transaction({'account': {'order_id': order.id}, 'amount': int(order.amount * 100)}, req_id)
        self.assertTrue(res1['result']['allow'])

        # 2. Create
        PaymentService.create_transaction({'id': payme_trans_id, 'account': {'order_id': order.id}, 'amount': int(order.amount * 100)}, req_id)

        # 3. Perform
        res3 = PaymentService.perform_transaction({'id': payme_trans_id}, req_id)
        self.assertEqual(res3['result']['state'], 2)

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)

    # TC-08: Muvaffaqiyatsiz to‘lov
    def test_tc08_payment_invalid_amount(self):
        order = Order.objects.create(listing=self.listing, buyer=self.buyer, amount=self.listing.price)
        res = PaymentService.check_perform_transaction({'account': {'order_id': order.id}, 'amount': 99999}, 'req_err')
        self.assertIn('error', res)

    # TC-09: Payme callback’ining takroriy yuborilishi (Idempotency)
    def test_tc09_payme_idempotency(self):
        order = Order.objects.create(listing=self.listing, buyer=self.buyer, amount=self.listing.price)
        payme_trans_id = 'payme_idempotent_1'
        PaymentService.create_transaction({'id': payme_trans_id, 'account': {'order_id': order.id}, 'amount': int(order.amount * 100)}, '1')
        PaymentService.perform_transaction({'id': payme_trans_id}, '2')

        # Repeat perform
        repeat_res = PaymentService.perform_transaction({'id': payme_trans_id}, '3')
        self.assertEqual(repeat_res['result']['state'], 2)
        self.assertEqual(Payment.objects.filter(payme_ref=payme_trans_id).count(), 1)

    # TC-10: Boshqa foydalanuvchi e‘lonini tahrirlashga urinish
    def test_tc10_unauthorized_listing_edit(self):
        with self.assertRaises(PermissionDenied):
            ListingService.update_listing(self.buyer, self.listing.id, title='Hacked Title')

    # TC-11: Oddiy foydalanuvchining admin sahifasiga kirishi
    def test_tc11_normal_user_admin_forbidden(self):
        self.client.force_login(self.buyer)
        response = self.client.get('/admin/')
        # Should redirect to admin login because buyer is not staff
        self.assertIn(response.status_code, [302, 403])

    # TC-12: AI xizmati ishlamaganda e‘lon qo‘shish
    def test_tc12_ai_fallback_manual_description(self):
        desc = AIService.improve_description('Old Phone', '')
        self.assertIn('sotiladi', desc)
