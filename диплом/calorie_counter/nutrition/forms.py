from django import forms
from .models import Product, ConsumedProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'calories', 'protein', 'fat', 'carbs']

class ConsumedProductForm(forms.ModelForm):
    class Meta:
        model = ConsumedProduct
        fields = ['product', 'weight']

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirm']:
            raise forms.ValidationError("Пароли не совпадают!")