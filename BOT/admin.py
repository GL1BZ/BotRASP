from django.contrib import admin

from .forms import UsersListForm
from .models import UsersList

@admin.register(UsersList)
class UsersListAdmin(admin.ModelAdmin):
    list_display = ('id', 'groupName', 'idUser', 'nameUser', 'alertStatus')
    form = UsersListForm

