"""
A module for tests in the clothes views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from .models import *
from clothes.models import Clothes, Category
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestViews(TestCase):

    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'ferg@567'

        self.category = Category.objects.create(name="test",
                                                friendly_name="test")
        self.item = Clothes.objects.create(name="Test", category=self.category,
                                           description="test description",
                                           has_sizes=True, price=2, rating=2,
                                           stock=2, on_sale=False,
                                           image_url="http://test.com",
                                           )

    # Test View Bag
    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='bag/bag.html')

    # Test Add to bag
    def test_add_to_bag(self):
        session = self.client.session
        redirect_link = f'/clothes/{self.item.id}/'
        response = self.client.post(f'/bag/add/{self.item.id}/',
                                    {'redirect_url': redirect_link
                                     })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Please select item size')                             

        response = self.client.post(f'/bag/add/{self.item.id}/',
                                    {'redirect_url': redirect_link,
                                     'item_size': 'M'})
        bag = self.client.session['bag']
        self.assertNotEqual(len(bag), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Added size M Test to your bag')
        response = self.client.post(f'/bag/add/{self.item.id}/',
                                    {'redirect_url': redirect_link,
                                     'item_size': 'M'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'Updated size M Test quantity to 2')
        # Test remove from bag
        response = self.client.post(f'/bag/remove/{self.item.id}/',
                                    {'redirect_url': redirect_link,
                                     'item_size': 'M'})
        messages = list(get_messages(response.wsgi_request))
        response = self.assertEqual(str(messages[3]), 'Removed size M Test from your bag')
        self.assertEqual(str(messages[3]), 'Removed size M Test from your bag')
        # Test adjust quantities
        response = self.client.post(f'/bag/add/{self.item.id}/',
                                    {'redirect_url': redirect_link,
                                     'item_size': 'M'})
        response = self.client.post(f'/bag/adjust/{self.item.id}/',
                                    {'item_size': 'M',
                                     'quantity': 10})
        messages = list(get_messages(response.wsgi_request))
        response = self.assertEqual(str(messages[5]), 'Updated size M Test quantity to 10')
        
