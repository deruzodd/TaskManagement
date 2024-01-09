from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from accounts.views import login_view, register_view, logout_view, \
    home_view, create_team, team_detail, add_team_member
from accounts.models import Team

''' Test urls '''


class URLTestClass(SimpleTestCase):
    def test_register_url(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func, register_view)

    def test_login_url(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_home_url(self):
        url = reverse('accounts:home')
        self.assertEqual(resolve(url).func, home_view)

    def test_create_team_url(self):
        url = reverse('accounts:create_team')
        self.assertEqual(resolve(url).func, create_team)

    def test_team_detail_url(self):
        url = reverse('accounts:team_detail', args=[1])
        self.assertEqual(resolve(url).func, team_detail)

    def test_add_team_member_url(self):
        url = reverse('accounts:add_team_member')
        self.assertEqual(resolve(url).func, add_team_member)


''' Test views'''


class ViewsTestClass(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.home_url = reverse('accounts:home')
        self.create_team = reverse('accounts:create_team')
        self.add_team_member = reverse('accounts:add_team_member')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_POST(self):
        """
        Check view when user registers with valid credentials
        """
        response = self.client.post(self.register_url, {
            'username': 'shubhadeep',
            'password1': 'deep1234',
            'password2': 'deep1234'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        # Successful redirect
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(response.context['user'].is_authenticated)

        # logout user
        self.client.logout()

        """
        Check view when user gives credentials 
        of an already registered user
        """
        response = self.client.post(self.register_url, {
            'username': 'shubhadeep',
            'pass1': 'deep1234',
            'pass2': 'deep1234'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        """
        Check view when user gives password that don't match
        """
        response = self.client.post(self.register_url, {
            'username': 'priyansh',
            'pass1': 'deep1235',
            'pass2': 'deep1234'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_POST(self):
        """
        Create test user
        """
        test_user = User.objects.create_user(
            username="priyansh", password="deep1234")

        """
        Check view when user gives correct credentials
        """
        response = self.client.post(self.login_url, {
            'username': 'priyansh',
            'password': 'deep1234'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(response.context['user'].is_authenticated)

        # logout user
        self.client.logout()

        """
        Check view when user gives wrong password
        """
        response = self.client.post(self.login_url, {
            'username': 'priyansh',
            'password': 'deep12345'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Check view when user gives wrong username
        """
        response = self.client.post(self.login_url, {
            'username': 'shubhadeep',
            'password': 'deep12345'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        del test_user

    def test_home_view(self):
        """
        Create test user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        url = reverse('accounts:home')

        """
        Try to access view without login
        """
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Try to access after login
        """
        self.client.post(self.login_url, credentials, follow=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        del test_user

    def test_logout_view(self):
        """
        Create new user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        """
        When user tries to access logout without login
        """
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        When user logs out after login
        """
        self.client.post(self.login_url, credentials, follow=True)
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        del test_user

    def test_create_team_view_GET(self):
        """
        Create new user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        """
        When user tries to access create team without login
        """
        response = self.client.get(self.create_team, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Access create_team after login
        """
        self.client.post(self.login_url, credentials)
        response = self.client.get(self.create_team, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_team.html')

        del test_user

    def test_create_team_view_POST(self):
        """
        Create new user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        """
        When user tries to access create team without login
        """
        response = self.client.post(self.create_team, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        When user submits post request after login
        """
        self.client.post(self.login_url, credentials)

        response = self.client.post(self.create_team, {
            'team_name': 'team 1'
        }, follow=True)

        team_length = Team.objects.count()
        team = Team.objects.get(team_name='team 1')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(team_length, 1)
        self.assertEqual(team.team_name, 'team 1')
        self.assertIn(test_user, team.members.all())

        del test_user

    def test_team_detail_view(self):
        """
        Create new user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        """
        When user tries to access create team without login
        """
        response = self.client.post(self.create_team, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Create team
        """
        self.client.post(self.login_url, credentials)
        self.client.post(self.create_team, {
            'team_name': 'team 1'
        }, follow=True)

        team = Team.objects.get(team_name='team 1')

        url = reverse('accounts:team_detail', args=[team.id])

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team_detail.html')

        del test_user

    def test_add_team_member(self):
        """
        Create new user
        """
        credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }

        test_user = User.objects.create_user(**credentials)

        """
        When user tries to access create team without login
        """
        response = self.client.post(self.add_team_member, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        When user logins, and gives invalid team_id
        """
        self.client.post(self.login_url, credentials, follow=True)
        response = self.client.post(self.add_team_member, {
            'team_id': 2
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        del test_user
