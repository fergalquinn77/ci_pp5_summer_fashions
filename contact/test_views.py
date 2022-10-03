"""
A module for tests in the clothes views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from .models import Contact
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestViews(TestCase):

    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'ferg@567'

    # Test Contact Us
    def test_contact_us(self):
        self.client.post('/contact/', {'email': self.email,
                         'name': self.username})
        contact = Contact.objects.count()
        self.assertEqual(contact, 1)
