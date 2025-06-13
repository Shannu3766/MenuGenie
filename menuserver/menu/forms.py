from django import forms
from .models import MenuItem, MenuSection

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['section', 'name', 'description', 'price', 'quantity', 'photo', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'min': '1'}),
        }

class MenuSectionForm(forms.ModelForm):
    class Meta:
        model = MenuSection
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter section name'}),
        } 