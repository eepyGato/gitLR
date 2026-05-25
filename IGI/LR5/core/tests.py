# core/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import (
    Branch, InsuranceType, InsuranceAgent, Client,
    InsuredObject, InsuranceContract, PromoCode, Review
)
import logging

logger = logging.getLogger(__name__)


class ModelTests(TestCase):
    """Tests for models"""
    
    def setUp(self):
        """Set up test data"""
        # Create branch
        self.branch = Branch.objects.create(
            name="Test Branch",
            address="Test Address",
            phone="+375 (29) 123-45-67"
        )
        
        # Create insurance type
        self.insurance_type = InsuranceType.objects.create(
            name="Test Insurance",
            commission_percent=10.00
        )
        
        # Create client user
        self.client_user = User.objects.create_user(
            username="testclient",
            password="testpass123",
            email="client@test.com"
        )
        
        # Create client profile
        self.client = Client.objects.create(
            user=self.client_user,
            first_name="Test",
            last_name="Client",
            address="Test Address",
            phone="+375 (29) 111-22-33",
            email="client@test.com",
            birth_date=date(1990, 1, 1),
            passport_number="AB1234567"
        )
        
        # Create agent user
        self.agent_user = User.objects.create_user(
            username="testagent",
            password="testpass123",
            email="agent@test.com"
        )
        
        # Create agent profile
        self.agent = InsuranceAgent.objects.create(
            user=self.agent_user,
            first_name="Test",
            last_name="Agent",
            address="Agent Address",
            phone="+375 (29) 444-55-66",
            birth_date=date(1985, 1, 1),
            branch=self.branch,
            hire_date=date(2020, 1, 1)
        )
        
        # Create insured object
        self.insured_object = InsuredObject.objects.create(
            client=self.client,
            object_type='car',
            description="Test Car",
            value=50000.00
        )
        
        # Create contract
        self.contract = InsuranceContract.objects.create(
            contract_number="TEST001",
            client=self.client,
            agent=self.agent,
            branch=self.branch,
            insurance_type=self.insurance_type,
            insured_object=self.insured_object,
            insurance_sum=100000.00,
            tariff_rate=5.00,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
    
    def test_branch_creation(self):
        """Test branch creation"""
        self.assertEqual(self.branch.name, "Test Branch")
        self.assertEqual(str(self.branch), "Test Branch")
    
    def test_insurance_type_creation(self):
        """Test insurance type creation"""
        self.assertEqual(self.insurance_type.name, "Test Insurance")
        self.assertEqual(self.insurance_type.commission_percent, 10.00)
    
    def test_client_age(self):
        """Test client age calculation"""
        age = self.client.age()
        self.assertGreaterEqual(age, 18)
    
    def test_client_age_validation(self):
        """Test client age validation (must be 18+)"""
        with self.assertRaises(Exception):
            underage_client = Client(
                first_name="Young",
                last_name="Person",
                address="Address",
                phone="+375 (29) 777-88-99",
                email="young@test.com",
                birth_date=date.today(),
                passport_number="CD1234567"
            )
            underage_client.save()
    
    def test_contract_calculation(self):
        """Test contract financial calculations"""
        payment = self.contract.insurance_payment()
        self.assertEqual(payment, 5000.00)  # 100000 * 5%
        
        commission = self.contract.agent_commission()
        self.assertEqual(commission, 500.00)  # 5000 * 10%
    
    def test_promo_code_validation(self):
        """Test promo code validation"""
        promo = PromoCode.objects.create(
            code="TEST50",
            discount_percent=50.00,
            valid_from=date.today() - timedelta(days=1),
            valid_to=date.today() + timedelta(days=30),
            max_uses=1
        )
        
        self.assertTrue(promo.is_valid())
        
        # Use promo code
        promo.used_count = 1
        promo.save()
        self.assertFalse(promo.is_valid())
    
    def test_review_creation(self):
        """Test review creation"""
        review = Review.objects.create(
            client=self.client,
            rating=5,
            text="Excellent service!",
            is_published=True
        )
        
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f"Отзыв {self.client} - 5/5")


class ViewTests(TestCase):
    """Tests for views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create branch
        self.branch = Branch.objects.create(
            name="Test Branch",
            address="Test Address",
            phone="+375 (29) 123-45-67"
        )
        
        # Create insurance type
        self.insurance_type = InsuranceType.objects.create(
            name="Test Insurance",
            commission_percent=10.00
        )
        
        # Create client user
        self.client_user = User.objects.create_user(
            username="testclient",
            password="testpass123",
            email="client@test.com"
        )
        
        # Create client profile
        self.client_profile = Client.objects.create(
            user=self.client_user,
            first_name="Test",
            last_name="Client",
            address="Test Address",
            phone="+375 (29) 111-22-33",
            email="client@test.com",
            birth_date=date(1990, 1, 1),
            passport_number="AB1234567"
        )
        
        # Create superuser
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass123",
            email="admin@test.com"
        )
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_page(self):
        """Test about page loads"""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_branches_page(self):
        """Test branches page loads"""
        response = self.client.get(reverse('core:branches'))
        self.assertEqual(response.status_code, 200)
    
    def test_contract_list_page(self):
        """Test contract list page loads"""
        response = self.client.get(reverse('core:contract_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_required_for_contract_create(self):
        """Test contract create requires login"""
        response = self.client.get(reverse('core:contract_create'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, '/login/?next=/contracts/create/')
    
    def test_admin_can_access_admin_panel(self):
        """Test admin can access admin panel"""
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        """Test registration page"""
        response = self.client.get(reverse('core:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_statistics_page(self):
        """Test statistics page loads"""
        response = self.client.get(reverse('core:statistics'))
        self.assertEqual(response.status_code, 200)
    
    def test_review_list_page(self):
        """Test review list page"""
        response = self.client.get(reverse('core:review_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_promo_codes_page(self):
        """Test promo codes page"""
        response = self.client.get(reverse('core:promo_codes'))
        self.assertEqual(response.status_code, 200)


class APITests(TestCase):
    """Tests for API endpoints"""
    
    def test_exchange_rate_api(self):
        """Test exchange rate API endpoint"""
        response = self.client.get(reverse('core:api_exchange_rate'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
    
    def test_weather_api(self):
        """Test weather API endpoint"""
        response = self.client.get(reverse('core:api_weather'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())


class FormTests(TestCase):
    """Tests for forms"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@test.com"
        )
    
    def test_valid_phone_number(self):
        """Test phone number validation"""
        from .forms import PhoneNumberMixin
        
        class TestForm(PhoneNumberMixin):
            def test_phone(self, phone):
                return self.validate_phone(phone)
        
        form = TestForm()
        valid_phone = "+375 (29) 123-45-67"
        invalid_phone = "123456"
        
        result = form.test_phone(valid_phone)
        self.assertEqual(result, valid_phone)
        
        with self.assertRaises(Exception):
            form.test_phone(invalid_phone)