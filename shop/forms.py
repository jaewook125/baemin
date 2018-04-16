from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review

		fields = ['rating', 'message', 'photo']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['address', 'phone']