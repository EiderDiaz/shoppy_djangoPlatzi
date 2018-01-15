from django.contrib import admin
from .models import Client
# Register your models here.
@admin.register(Client)
class AdminClient(admin.ModelAdmin):
	list_display = ('name','phone','email','address',)
	list_filter = ('name',)

