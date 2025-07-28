from django import forms
from .models import Product, ConsumedProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'calories', 'protein', 'fat', 'carbs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название продукта',
            'calories': 'Калории (ккал)',
            'protein': 'Белки (г)',
            'fat': 'Жиры (г)',
            'carbs': 'Углеводы (г)',
        }

class ConsumedProductForm(forms.ModelForm):
    class Meta:
        model = ConsumedProduct
        fields = ['product', 'weight']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'product': 'Продукт',
            'weight': 'Вес (г)',
        }

    def __init__(self, user, *args, **kwargs):
        super(ConsumedProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(user=user)

class UserRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Подтвердите пароль"
    )

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirm']:
            raise forms.ValidationError("Пароли не совпадают!")