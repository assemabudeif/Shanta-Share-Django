from django.contrib import admin

from core.models import Driver, Client, City, Government

# Register your models here.


admin.site.register(Driver)
admin.site.register(Client)
admin.site.register(City)
admin.site.register(Government)