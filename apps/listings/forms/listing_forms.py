from django import forms
from apps.listings.models import Listing
from apps.categories.models import Category

class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label="Kategoriyani tanlang"
    )

    class Meta:
        model = Listing
        fields = ['title', 'category', 'price', 'city', 'address', 'lat', 'lng', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: iPhone 15 Pro Max 256GB'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Toshkent shahar'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chilonzor tumani, 9-mavze'}),
            'lat': forms.HiddenInput(attrs={'id': 'id_lat'}),
            'lng': forms.HiddenInput(attrs={'id': 'id_lng'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mahsulot haqida to‘liq ma‘lumot...'}),
        }
