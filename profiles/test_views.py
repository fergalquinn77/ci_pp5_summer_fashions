"""
A module for tests in the profile views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from .models import Support_Tickets, Tickets_Messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestViews(TestCase):

    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'ferg@567'

    # Test User Registration Page
    def test_signup_page_url(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/signup.html')

    # Test User Signup
    def test_signup_form(self):
        response = self.client.post(reverse('account_signup'), data={
            'email': self.email,
            'email2': self.email,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    # Test cannot user display tickets without login
    def test_display_tickets_without_login(self):
        response = self.client.get(reverse('open-support-tickets'))
        self.assertEqual(response.status_code, 302)

    # Test can user display tickets with login
    def test_display_tickets_with_login(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        response = self.client.get(reverse('open-support-tickets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='profiles/support.html')

    # Test can user add ticket when logged in
    def test_add_support_ticket_with_login(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        response = self.client.get(reverse('add-support-ticket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='profiles/add_ticket.html')
        response2 = self.client.post(reverse('add-support-ticket'),
                                     {'title': 'Test New Query',
                                     'query': 'Test message'})
        self.assertEqual(response2.status_code, 302)
        tickets = Support_Tickets.objects.all()
        self.assertEqual(tickets.count(), 1)

    # Test can user view ticket details page
    def test_ticket_details(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        self.client.post(reverse('add-support-ticket'),
                         {'title': 'Test New Query',
                         'query': 'Test message'})
        ticket = Support_Tickets.objects.get(title='Test New Query')
        response = self.client.get(f'/profile/ticket-details/{ticket.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='profiles/ticket_detail.html')

    # Test Toggle Ticket
    def test_toggle_ticket(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        self.client.post(reverse('add-support-ticket'),
                         {'title': 'Test New Query',
                         'query': 'Test message'})
        ticket = Support_Tickets.objects.get(title='Test New Query')
        self.assertEqual(ticket.status, 0)
        response = self.client.get((f'/profile/toggle-ticket-status'
                                   f'/{ticket.id}/'))
        updated_ticket = Support_Tickets.objects.get(title='Test New Query')
        self.assertEqual(updated_ticket.status, 1)

    # Test Posting Message on ticket details page

    def test_post_message(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        self.client.post('/profile/add-ticket/', {'title': 'Test New Query',
                         'query': 'Test message'})
        ticket = Support_Tickets.objects.get(title='Test New Query')
        response = self.client.post(f'/profile/ticket-details/{ticket.id}/',
                                    {'message': 'Test Message'})
        message = Tickets_Messages.objects.get(ticket=ticket.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(message.message, 'Test Message')
