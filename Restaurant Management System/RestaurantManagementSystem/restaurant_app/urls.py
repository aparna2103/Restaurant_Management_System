from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('foodmenu/', views.foodmenu, name='foodmenu'),
    path('table-booking/', views.table_booking, name='table-booking'),
    path('order-history/', views.order_history, name='order-history'),
    path('edit-menu/', views.editmenu, name='edit-menu'),
    path('deleteFoodItem', views.deleteFoodItem, name='deleteFoodItem'),
    path('saveEditedItem', views.saveEditedItem, name='saveEditedItem'),
    path('addFoodItem', views.addFoodItem, name='addFoodItem'),
    path('viewusers', views.viewusers, name='viewusers'),
    path('tableslist/', views.tableslist, name='tableslist'),
    path('addTable', views.addTable, name='addTable'),
    path('changeTableAvailability', views.changeTableAvailability, name='changeTableAvailability'),
    path('orderFood', views.orderFood, name='orderFood'),
    path('bookTable', views.bookTable, name='bookTable'),
    path('savepaymentinfo', views.userPaymentInfo, name='savepaymentinfo'),
    # path('view-users/', views.viewusers, name='view-users'),
]