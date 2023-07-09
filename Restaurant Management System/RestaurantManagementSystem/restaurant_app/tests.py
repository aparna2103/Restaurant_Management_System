from django.test import SimpleTestCase
from django.urls import reverse, resolve
from restaurant_app.views import *
from django.test import TestCase, Client
from restaurant_app.models import *
import json
import random, string

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_foodmenu_url_is_resolved(self):
        url = reverse('foodmenu')
        self.assertEquals(resolve(url).func, foodmenu)

    def test_paymentdetails_url_is_resolved(self):
        url = reverse('savepaymentinfo')
        self.assertEquals(resolve(url).func, userPaymentInfo)

    def test_table_booking_url_is_resolved(self):
        url = reverse('table-booking')
        self.assertEquals(resolve(url).func, table_booking)

    def test_order_history_url_is_resolved(self):
        url = reverse('order-history')
        self.assertEquals(resolve(url).func, order_history)
    
    def test_edit_menu_url_is_resolved(self):
        url = reverse('edit-menu')
        self.assertEquals(resolve(url).func, editmenu)

    def test_deleteFoodItem_url_is_resolved(self):
        url = reverse('deleteFoodItem')
        self.assertEquals(resolve(url).func, deleteFoodItem)

    def test_saveEditedItem_url_is_resolved(self):
        url = reverse('saveEditedItem')
        self.assertEquals(resolve(url).func, saveEditedItem)

    def test_addFoodItem_url_is_resolved(self):
        url = reverse('addFoodItem')
        self.assertEquals(resolve(url).func, addFoodItem)

    def test_viewusers_url_is_resolved(self):
        url = reverse('viewusers')
        self.assertEquals(resolve(url).func, viewusers)

    def test_tableslist_url_is_resolved(self):
        url = reverse('tableslist')
        self.assertEquals(resolve(url).func, tableslist)

    def test_addTable_url_is_resolved(self):
        url = reverse('addTable')
        self.assertEquals(resolve(url).func, addTable)

    def test_changeTableAvailability_url_is_resolved(self):
        url = reverse('changeTableAvailability')
        self.assertEquals(resolve(url).func, changeTableAvailability)

    def test_orderFood_url_is_resolved(self):
        url = reverse('orderFood')
        self.assertEquals(resolve(url).func, orderFood)

    def test_bookTable_url_is_resolved(self):
        url = reverse('bookTable')
        self.assertEquals(resolve(url).func, bookTable)

class TestModels(TestCase):

    def setUp(self):
        self.food1 = FoodItemsTable.objects.create(
            dish_name = 'Cake',
            dish_description = 'dessert',
            dish_price = 15
        )

        self.user = UserTable.objects.create(
            full_name = "Aparna",
            username = "aparna53",
            email = "email@email.com",
            address = "gh",
            contact_number = 789,
            role = 1
        )

        self.table = TableAvailability.objects.create(
            table_type = "2 seater",
            status = "available",
        )

        self.table1 = TableBooking.objects.create(
           booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5)),
           table_id = self.table,
           user_id = self.user.id
        )

        self.foodTable = FoodOrderTable.objects.create(
            order_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            item_id = self.food1,
            quantity = 3,
            total_price = 30,
            user_id = self.user
        )

        self.paymentTable = UserPaymentInformation.objects.create(
            user_id = self.user,
            cardnumber = "6739273894617362",
            cvv = "736"
        )


    def test_food_is_assigned_on_creation(self):
        self.assertEquals(self.food1.dish_name, 'Cake')
        self.assertEquals(self.food1.dish_description, 'dessert')
        self.assertEquals(self.food1.dish_price, 15)

    def test_user_is_assigned_on_creation(self):
        self.assertEquals(self.user.full_name, 'Aparna')
        self.assertEquals(self.user.username, 'aparna53')
        self.assertEquals(self.user.email, 'email@email.com')
        self.assertEquals(self.user.address, 'gh')
        self.assertEquals(self.user.contact_number, 789)
        self.assertEquals(self.user.role, 1)

    def test_table_is_assigned_on_creation(self):
        self.assertEquals(self.table.table_type, '2 seater')
        self.assertEquals(self.table.status, 'available')

    def test_food_order_table_is_assigned_on_creation(self):
        self.assertEquals(self.foodTable.quantity, 3)
        self.assertEquals(self.foodTable.total_price, 30)

    def test_payment_table_is_assigned_on_creation(self):
        self.assertEquals(self.paymentTable.cardnumber, '6739273894617362')
        self.assertEquals(self.paymentTable.cvv, '736')
    
# class TestViews(TestCase):

#     def test_foodmenu_GET(self):
#         client = Client()

#         response = client.get(reverse('foodmenu'))

#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'restaurant_app/food_menu.html')
      






