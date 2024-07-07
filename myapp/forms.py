from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect,
        }
        labels = {
            'member': u'Member name',
        }


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices = FEEDBACK_CHOICES)


class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='Your Name')
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect, required=False, label='Select a category:')
    max_price = forms.IntegerField(label='What Price', min_value=0)