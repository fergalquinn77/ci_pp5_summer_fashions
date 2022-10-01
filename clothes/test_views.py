"""
A module for tests in the clothes views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from .models import *
from django.contrib.auth import get_user_model
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

    # Test View all page
    def test_view_all(self):
        response = self.client.get(reverse('clothes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='clothes/clothes.html')

    # Test View item details page
    def test_view_all(self):
        response = self.client.get(f'/clothes/{self.item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='clothes/item_details.html')

    # Test add item details page (without login)
    def test_add_item_no_login(self):
        response = self.client.get(reverse('add_item'))
        self.assertEqual(response.status_code, 302)

    # Test add item details page (with normal user login)
    def test_add_item_normal_user(self):
        user = User.objects.create_user(self.username, self.email,
                                        self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('add_item'))
        self.assertEqual(response.status_code, 302)

    # Test add item details page (with admin login)
    def test_add_item_admin_user(self):
        user = User.objects.create_superuser(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('add_item'))
        self.assertEqual(response.status_code, 200)

    # Test edit item details page (without login)
    def test_edit_item_no_login(self):
        response = self.client.get(f'/clothes/edit/{self.item.id}/')
        self.assertEqual(response.status_code, 302)

    # Test edit item details page (with normal user login)
    def test_edit_item_normal_user(self):
        user = User.objects.create_user(self.username, self.email,
                                        self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(f'/clothes/edit/{self.item.id}/')
        self.assertEqual(response.status_code, 302)

    # Test edit item details page (with admin login)
    def test_edit_item_admin_user(self):
        user = User.objects.create_superuser(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(f'/clothes/edit/{self.item.id}/')
        self.assertEqual(response.status_code, 200)
        item = Clothes.objects.create(
            name=self.item.name,
            category=self.item.category,
            description=self.item.description,
            has_sizes=self.item.has_sizes,
            price=self.item.price,
            rating=self.item.rating,
            stock=self.item.stock,
            on_sale=self.item.on_sale)

        self.client.post(f'/clothes/edit/{item.id}/',
                         {
                          'name': self.item.name,
                          'category': self.item.category,
                          'description': 'change',
                          'has_sizes': self.item.has_sizes,
                          'price': self.item.price,
                          'rating': self.item.rating,
                          'stock': self.item.stock,
                          'on_sale': self.item.on_sale,
                          }
                         )
        item_updated = Clothes.objects.get(id=item.id)
        # self.assertEqual(item_updated.description, "change")

    # Test delete item details page (without login)
    def test_delete_item_no_login(self):
        response = self.client.get(f'/clothes/delete/{self.item.id}/')
        self.assertEqual(response.status_code, 302)
        updated_item = Clothes.objects.filter(id=self.item.id)
        self.assertEqual(updated_item.count(), 1)

    # Test delete item details page (with normal user login)
    def test_delete_item_normal_user(self):
        user = User.objects.create_user(self.username, self.email,
                                        self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(f'/clothes/delete/{self.item.id}/')
        self.assertEqual(response.status_code, 302)
        updated_item = Clothes.objects.filter(id=self.item.id)
        self.assertEqual(updated_item.count(), 1)

    # Test delete item details page (with admin login)
    def test_delete_item_admin_user(self):
        user = User.objects.create_superuser(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        id = self.item.id
        response = self.client.get(f'/clothes/delete/{self.item.id}/')
        self.assertEqual(response.status_code, 302)
        updated_item = Clothes.objects.filter(id=id)
        self.assertEqual(updated_item.count(), 0)

    # Add and remove to wishlist - Toggle Wishlist
    def test_add_remove_wishlist(self):
        user = User.objects.create_user(self.username, self.email,
                                        self.password)
        self.client.login(username=self.username, password=self.password)
        redirect_url = reverse('clothes')
        response = self.client.post(f'/clothes/togglewish/{self.item.id}/',
                                    HTTP_REFERER=redirect_url)
        self.assertEqual(response.status_code, 302)
        wishlist_exists = self.item.wishlists.filter(id=user.id)
        self.assertNotEqual(wishlist_exists.count(), 0)
        response = self.client.post(f'/clothes/togglewish/{self.item.id}/',
                                    HTTP_REFERER=redirect_url)
        wishlist_exists = self.item.wishlists.filter(id=user.id)
        self.assertEqual(wishlist_exists.count(), 0)

    # View Wishlist
    def test_wishlist_view(self):
        # Not logged in
        response = self.client.get(reverse('view_wishlist'))
        self.assertEqual(response.status_code, 302)
        user = User.objects.create_user(self.username, self.email,
                                        self.password)
        self.client.login(username=self.username, password=self.password)
        redirect_url = reverse('clothes')
        response2 = self.client.get(reverse('view_wishlist'))
        self.assertEqual(response2.status_code, 200)

    # Toggle Sale Status
    def test_toggle_sale_status(self):
        # Not logged in
        self.assertEqual(self.item.on_sale, False)
        redirect_url = f'/clothes/{self.item.id}/'
        self.client.post(f'/clothes/sale/{self.item.id}/',
                         HTTP_REFERER=redirect_url)
        updated_item = Clothes.objects.get(id=self.item.id)
        self.assertEqual(updated_item.on_sale, False)
        user = User.objects.create_superuser(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.get(f'/clothes/{self.item.id}/')
        self.client.post(f'/clothes/sale/{self.item.id}/',
                         HTTP_REFERER=redirect_url)
        updated_item = Clothes.objects.get(id=self.item.id)
        self.assertEqual(updated_item.on_sale, True)
        self.client.post(f'/clothes/sale/{self.item.id}/',
                         HTTP_REFERER=redirect_url)
        updated_item = Clothes.objects.get(id=self.item.id)
        self.assertEqual(updated_item.on_sale, False)

    # Update Sales Percentage
    def test_update_sales_percent(self):
        redirect_url = f'/clothes/{self.item.id}/'
        user = User.objects.create_superuser(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(f'/clothes/update/{self.item.id}/',
                                    {'discount': 10},
                                    HTTP_REFERER=redirect_url)
        self.assertEqual(self.item.sale.percent_off, 10)
