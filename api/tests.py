from django.contrib.auth import get_user_model
from django.http import response
from django.utils.timezone import localtime
from rest_framework.test import APITestCase
# from rest_framework.simplejwt.tokens import RefreshToken

from .models import Book


class TestBookCreateAPI(APITestCase):

    TARGET_URL = '/api/books/'

    def test_create_success(self):
        params = {
            'title': 'APIの本',
            'price': 1200,
        }

        response = self.client.post(self.TARGET_URL, params, format='json')

        # testing
        self.assertEqual(Book.objects.count(), 1)

        self.assertEqual(response.status_code, 201)

        book = Book.objects.get()
        expected_json_dict = {
            'id':str(book.id),
            'title': book.title,
            'price': book.price,
            'created_at':str(localtime(book.created_at)).replace(' ', 'T'),
        }

        print(vars(book))

        self.assertEqual(params["title"], book.title)
