from .models import Customers,Books,Loans
from django.forms import ModelForm
from django import forms


class CustomerForm(ModelForm):
     class Meta:
         model = Customers
         fields = ['name', 'city', 'age']

class BookForm(ModelForm):
     class Meta:
         model = Books
         fields = ['name', 'author', 'year_published','type']

class LoanForm(ModelForm):
    loan_date = forms.DateTimeField(input_formats='%Y-%m-%d')
    return_date = forms.DateTimeField(input_formats='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['customer'].widget.attrs['disabled'] = "disabled"
            self.fields['customer'].required = False
            self.fields['book'].widget.attrs['disabled'] = "disabled"
            self.fields['book'].required = False
            self.fields['loan_date'].widget.attrs['readonly'] = True
            self.fields['loan_date'].required = False
            # self.fields['buyer'].widget.attrs['disabled'] = "disabled"
        else:
            from django.forms.widgets import HiddenInput
            hide_condition = self.fields.get('return_date')
            super(LoanForm, self).__init__(*args, **kwargs)
            if hide_condition:
                self.fields['return_date'].required = False
                self.fields['return_date'].widget = HiddenInput()

    def clean_customer(self):
        instance = getattr(self, 'instance', None)
        if instance.pk is not None :
            return instance.customer
        else:
            return self.cleaned_data.get('customer', None)
    
    def clean_book(self):
        instance = getattr(self, 'instance', None)
        if instance.pk is not None:
            return instance.book
        else:
            return self.cleaned_data.get('book', None)

    def clean_loan_date(self):
        instance = getattr(self, 'instance', None)
        if instance.pk is not None:
            return instance.loan_date
        else:
            return self.cleaned_data.get('loan_date', None)

    class Meta:
         model = Loans
         fields = ['customer', 'book', 'loan_date','return_date']
