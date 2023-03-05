from django import forms

from .models import UsersList

class UsersListForm(forms.ModelForm):
    class Meta:
        model = UsersList
        fields = (
            'groupName',
            'idUser',
            'nameUser',
            'alertStatus',
        )
        widgets = {
            'groupName': forms.TextInput,
            'idUser': forms.TextInput,
            'nameUser': forms.TextInput,
            'alertStatus': forms.TextInput,
        }