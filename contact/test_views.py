"""
A module for tests in the clothes views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from .models import *
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestViews(TestCase):

    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'ferg@567'

    # Test Contact Us
    def test_contact_us(self):
        response = self.client.post(f'/contact/', {'email': self.email,
                                    'name': self.username})
        contact = Contact.objects.count()
        self.assertEqual(contact, 1)
