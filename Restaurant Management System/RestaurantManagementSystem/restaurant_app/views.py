from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import *
import logging

logger = logging.getLogger(__name__)


@login_required(login_url="/login")
@check_perm
def home(request):
    return render(request, 'restaurant_app/home.html')

@login_required(login_url="/login")
@check_perm
def foodmenu(request):
    try:
        logger.debug("Entered food menu")
        food_items = FoodItemsTable.get_food_items()
        data = {
            "food_items": food_items
        }
    except Exception as e:
        logger.debug("Request for food menu failed")
    return render(request, 'restaurant_app/food_menu.html', data)


@login_required(login_url="/login")
@check_perm
def table_booking(request):
    try:
        logger.debug("Customer Tables viewing request sent")
        available_tables = TableAvailability.get_available_tables()
        data = {
            "tables": available_tables
        }
    except Exception as e:
         logger.debug("Customer Tables viewing request failed")
    return render(request, 'restaurant_app/table-booking.html', data)

@login_required(login_url="/login")
@check_perm
def order_history(request):
    try:
        logger.debug("Request for viewing the order history sent")
        orders = FoodOrderTable.get_orders(request.user)
    except Exception as e:
        logger.debug("Request for viewing the order history failed")
    return render(request, 'restaurant_app/order-history.html', {"orders": orders})


def sign_up(request):
    try:
        logger.debug("Request for loading the sign-up sent")
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(request.POST["password1"])
                user.save()
                # login(request, user)
                return redirect('/login')
        else:
            form = RegisterForm()
    except Exception as e:
        logger.debug("Sign-up page request failed")
    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
@check_perm
def editmenu(request):
    try:
        logger.debug("Request for editing food menu sent")
        food_items = FoodItemsTable.get_food_items()
        data = {
            "food_items": food_items
        }
    except Exception as e:
        logger.debug("Editing the food menu request failed")
    return render(request, 'manager/editmenu.html', data)

@check_perm
def deleteFoodItem(request):
    try:
        logger.debug("Request for deleting a food item sent")
        food_id = request.POST["food_id"]
        FoodItemsTable.delete_food(food_id)
    except Exception as e:
        logger.debug("Deleting a food item request failed")
    return JsonResponse({"msg": "Deletion Success!"})

@check_perm
def saveEditedItem(request):
    try:
        logger.debug("Request for saving a new food item in the menu sent")
        FoodItemsTable.edit_food(request)
    except Exception as e:
        logger.debug("Saving a new food item in the menu request failed")
    return JsonResponse({"msg": "Deletion Success!"})

@check_perm
def addFoodItem(request):
    try:
        logger.debug("Request for adding a food item in the cart sent")
        FoodItemsTable.addFood(request)
    except Exception as e:
        logger.debug("Request for adding a food item in the cart failed")
    return JsonResponse({"msg": "Deletion Success!"})

@check_perm
def viewusers(request):
    try:
        logger.debug("Request for viewing customer details sent")
        users = UserTable.getAllUsers()
        data = {
            "users": users
        }
    except Exception as e:
        logger.debug("Request for viewing customer details failed")
    return render(request, 'manager/viewcustomers.html', data)

@check_perm
def tableslist(request):
    try:
        logger.debug("Manager's request for viewing all the tables sent")
        tables = TableAvailability.getAllTabels()
        data = {
            "tables": tables
        }
    except Exception as e:
        logger.debug("Manager's request for viewing all the tables failed")
    return render(request, 'manager/table_list.html', data)

@check_perm
def addTable(request):
    try:
        logger.debug("Request for adding new tables sent")
        tables = TableAvailability.addTable(request)
    except Exception as e:
        logger.debug("Request for adding new tables failed")
    return JsonResponse({"msg": "Deletion Success!"})

@check_perm
def changeTableAvailability(request):
    try:
        logger.debug("Request for changing table availability sent")
        TableAvailability.change_availability(request)
    except Exception as e:
        logger.debug("Request for changing table availability failed")
    return JsonResponse({"msg": "Deletion Success!"})

@check_perm
def orderFood(request):
    try:
        logger.debug("Request for ordering food sent")
        FoodOrderTable.orderfood(request)
    except Exception as e:
        logger.debug("Request for ordering food failed")
    return JsonResponse({"msg": "Ordered!"})

@check_perm
def bookTable(request):
    try:
        logger.debug("Request for booking a table sent")
        TableBooking.bookTable(request)
    except Exception as e:
        logger.debug("Request for booking a table failed")
    return JsonResponse({"msg": "Ordered!"})

@login_required(login_url='/salesapp/login/')
@check_perm
def userPaymentInfo(request):
    try:
        logger.debug("Request for saving the user's payment information sent")
        data = {"payment_details_exist": False}
        if request.method == "POST":
            form = UserPaymentDetails(request.POST, instance=request.user)
            data["form"] = form
            if form.is_valid():
                UserPaymentInformation.create_payment_info(form.cleaned_data, form.instance)
                # messages.success(request, "Payment information saved")
                return redirect('/home')
        else:
            if UserPaymentInformation.payment_details_exist(request.user):
                data["payment_details_exist"] = True
                data["payment_details"] = UserPaymentInformation.get_payment_details(request.user)
            else:
                data["form"] = UserPaymentDetails()
    except Exception as e:
        logger.debug("Request for saving the user's payment information failed")
    return render(request, 'restaurant_app/user_payment_info.html', data)