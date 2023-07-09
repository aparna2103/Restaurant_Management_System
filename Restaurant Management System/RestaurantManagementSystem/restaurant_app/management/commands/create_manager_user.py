from django.core.management.base import BaseCommand, CommandError
from restaurant_app.models import UserTable
 
class Command(BaseCommand):
    help = 'Creating Admin user'
 
    def handle(self, *args, **options):
        username = "Manager"
        full_name = "Aparna Gupta"
        email="manager@admin.com"
        
 
        admin_user = UserTable.objects.create(username=username, email=email, role=2, full_name=full_name,
        address="Graduate Hills", contact_number=123456)
        admin_user.set_password("Abcd!@#$")
        admin_user.save()
 
        print("Manager user created.......")