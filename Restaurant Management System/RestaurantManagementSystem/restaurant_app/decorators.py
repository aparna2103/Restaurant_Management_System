from django.core.exceptions import PermissionDenied
 
customer_perm = ["home", "foodmenu", "table_booking", "order_history", "orderFood", "bookTable", "userPaymentInfo"]
 
manager_perm = ["home", "editmenu", "deleteFoodItem", "saveEditedItem", "addFoodItem", "viewusers", "tableslist", "addTable", 
"changeTableAvailability"]

def check_perm(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        func_name = function.__name__
        if user.has_perm(func_name):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap