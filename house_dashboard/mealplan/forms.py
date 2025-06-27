from django import forms
from .models import GroceryItem

class GroceryItemForm(forms.ModelForm):
    class Meta:
        model = GroceryItem
        fields = ['title'] # Customize based on your model
