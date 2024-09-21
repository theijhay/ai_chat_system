from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from chat.models import User, Chat

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().tokens, 4000)  # Default tokens


class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class ChatTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.login()

    def login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_chat(self):
        url = reverse('chat')
        data = {
            'message': 'Hello AI'
        }

        """Ensure there are no chats initially"""
        self.assertEqual(Chat.objects.count(), 0)

        """Post a message to the chat endpoint"""
        response = self.client.post(url, data, format='json')

        """Check response status and content"""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello AI')
        self.assertEqual(response.data['response'], 'This is a dummy response.')  # Based on the dummy response logic
        self.assertEqual(response.data['remaining_tokens'], 3900)  # 100 tokens deducted

        """Check that the chat has been saved to the database"""
        self.assertEqual(Chat.objects.count(), 1)  # One chat should now be saved

        chat = Chat.objects.first()  # Get the saved chat
        self.assertEqual(chat.message, 'Hello AI')  # Check if the message matches
        self.assertEqual(chat.response, 'This is a dummy response.')  # Check if the response matches
        self.assertEqual(chat.user, self.user)  # Check if the correct user is associated with the chat
        
class TokenBalanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', tokens=3500)
        self.client = APIClient()
        self.login()

    def login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_token_balance(self):
        url = reverse('token-balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tokens'], 3500)
        
class TokenTopUpTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', tokens=3500)
        self.client = APIClient()
        self.login()

    def login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_token_top_up(self):
        url = reverse('token-top-up')
        data = {
            'tokens': 500
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tokens'], 4000)  # 3500 + 500 tokens
