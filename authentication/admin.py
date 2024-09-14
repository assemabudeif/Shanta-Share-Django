from django.contrib import admin
from .models import BaseUser, Driver, Client
# Register your core_models here.


admin.site.register(BaseUser)
admin.site.register(Driver)
admin.site.register(Client)
