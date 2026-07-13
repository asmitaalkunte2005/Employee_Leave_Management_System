from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.admin_user = self.user_model.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
        )
        self.employee_user = self.user_model.objects.create_user(
            username='employeeuser',
            email='employee@example.com',
            password='employeepass123',
        )

    def test_root_url_shows_login_page(self):
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Employee Leave Management System')

    def test_admin_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('login_page'),
            {'username': 'adminuser', 'password': 'adminpass123'},
            follow=True,
        )
        self.assertRedirects(response, reverse('home'))

    def test_employee_login_redirects_to_employee_dashboard(self):
        response = self.client.post(
            reverse('login_page'),
            {'username': 'employeeuser', 'password': 'employeepass123'},
            follow=True,
        )
        self.assertRedirects(response, reverse('employee_dashboard'))
