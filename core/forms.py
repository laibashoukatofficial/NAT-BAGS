from django import forms
from stripe import Review 
from core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

class PaymentMethodForm(forms.Form):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)
    
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact_phone = forms.CharField(max_length=15)
    shipping_address = forms.CharField(widget=forms.Textarea)
    billing_address = forms.CharField(widget=forms.Textarea, required=False)
    payment_method = forms.ChoiceField(choices=[('cod', 'Cash on Delivery')], widget=forms.RadioSelect)







