from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string
import json
import hashlib
from django.core.validators import MinLengthValidator
from django.db.models import Count
from .decorators import manager_perm, customer_perm

# Create your models here.

class FoodItemsTable(models.Model):
    dish_name = models.CharField(max_length=50, unique=True)
    dish_description = models.CharField(max_length=100)
    dish_price = models.IntegerField()

    @classmethod
    def get_food_items(cls):
        return cls.objects.values()

    @classmethod
    def delete_food(cls, foodid):
        cls.objects.get(id=foodid).delete()

    @classmethod
    def edit_food(cls, request):
        dish_name = request.POST["dish_name"]
        dish_description = request.POST["dish_des"]
        dish_price = request.POST["dish_price"]
        dish_id = request.POST["dish_id"]

        dish = cls.objects.get(id=dish_id)
        dish.dish_name = dish_name
        dish.dish_description = dish_description
        dish.dish_price = dish_price
        dish.save()

    @classmethod
    def addFood(cls, request):
        dish_name = request.POST["dish_name"]
        dish_description = request.POST["dish_des"]
        dish_price = request.POST["dish_price"]

        dish = cls.objects.create(dish_name=dish_name, dish_description=dish_description, dish_price=dish_price)
        dish.save()

class UserTable(AbstractUser):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=80, unique=True)
    address = models.CharField(max_length=500)
    contact_number = models.IntegerField(null=True)
    role = models.PositiveIntegerField(default=1)

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.full_name
 
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.role == 1:
            if not perm in customer_perm: return False
        elif self.role == 2:
            if not perm in manager_perm: return False
        return True

    @classmethod
    def create_manager(cls):
        manager = cls.objects.create(username="aparna_", full_name="Aparna Gupta", email="agupta53@ud.edu", address="Graduate Hill Apts", contact_number=27634748)
        manager.set_password("Abcd!@#$")
        manager.save()

    @classmethod
    def getAllUsers(cls):
        return list(cls.objects.filter(role=1).values("full_name", "email", "address", "contact_number", "id"))

class TableAvailability(models.Model):
    table_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)    #booked or available

    @classmethod
    def getAllTabels(cls):
        return list(cls.objects.values("table_type", "status", "id"))

    @classmethod
    def addTable(cls, request):
        table_type = request.POST["table_type"]
        cls.objects.create(table_type=table_type, status="Available")
    
    @classmethod
    def change_availability(cls, request):
        table = cls.objects.get(id=request.POST["table_id"])
        table.status = "Available" if table.status == "Booked" else "Booked"
        table.save()

    @classmethod
    def get_available_tables(cls):
        return list(cls.objects.filter(status="Available").values("table_type", "id"))

class TableBooking(models.Model):
    booking_id = models.CharField(max_length=5, unique=True, default=''.join(random.choices(string.ascii_letters + string.digits, k=5)))
    table_id = models.ForeignKey(TableAvailability, on_delete=models.CASCADE) #table availability S.No
    user_id = models.IntegerField() #user S.No

    @classmethod
    def bookTable(cls, request):
        table_id = TableAvailability.objects.get(id=request.POST["table_id"])
        table_id.status = "Booked"
        table_id.save()
        cls.objects.create(table_id=table_id, user_id=request.user.id, booking_id=''.join(random.choices(string.ascii_letters + string.digits, k=5)))

class FoodOrderTable(models.Model):
    order_id = models.CharField(max_length=8, default=''.join(random.choices(string.ascii_letters + string.digits, k=8)))
    item_id = models.ForeignKey(FoodItemsTable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    user_id = models.ForeignKey(UserTable, on_delete=models.CASCADE)

    @classmethod
    def get_orders(cls, user):
        orders = {}
        qs = FoodOrderTable.objects.filter(user_id=user).values("order_id", "item_id__dish_name", "quantity", "total_price").annotate(count=Count('order_id'))
        for order in qs:
            item = {"dish_name": order["item_id__dish_name"], "quantity": order["quantity"], "total_price": order["total_price"]}
            if not order["order_id"] in orders: orders[order["order_id"]] = []
            orders[order["order_id"]].append(item)
        return orders


    @classmethod
    def orderfood(cls, request):
        food_items = json.loads(request.POST["foodjson"])
        user = request.user
        order_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        for food in food_items:
            dish = FoodItemsTable.objects.get(dish_name=food["foodName"])
            cls.objects.create(item_id=dish, user_id=user, total_price=food["totalPrice"], quantity=food["quantity"], order_id=order_id)

class UserPaymentInformation(models.Model):
    user_id = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    cardnumber = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    cvv = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    @classmethod
    def get_payment_details(cls, user):
        return cls.objects.filter(user_id=user).values("cardnumber")[0]

    @classmethod
    def create_payment_info(cls, data, user):
        try:
            cls.objects.get(user_id=user)
        except UserPaymentInformation.DoesNotExist:
            cardnumber = data['cardnumber'][-4:]
            cvv = hashlib.sha256(data['cvv'].encode('utf-8')).hexdigest()
            UserPaymentInformation.objects.create(cardnumber=cardnumber, cvv=cvv, user_id=user)

    @classmethod
    def payment_details_exist(cls, user):
        try:
            cls.objects.get(user_id=user)
        except UserPaymentInformation.DoesNotExist:
            return False
        return True