from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Transfer, Chatbox

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email Address")
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['account_number', 'amount', 'holder_name', 'bank_name', 'description', 'transaction_pin']
        widgets = {
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Account Number',
            }),
            'holder_name': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Holder Name',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Amount',
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Bank Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Description (Optional)',
                'rows': 3,
            }),
            'transaction_pin': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 4-digit PIN',
            }),
        }
        labels = {
            'account_number': 'Account Number',
            'holder_name': 'Holder Name',
            'amount': 'Amount',
            'bank_name': 'Bank Name',
            'description': 'Description',
            'transaction_pin': 'Transaction PIN',
        }

    def clean_transaction_pin(self):
        pin = self.cleaned_data.get('transaction_pin')
        if len(str(pin)) != 4:
            raise forms.ValidationError("Transaction PIN must be correct exactly 4 digits.")
        return pin
    


class MessageForm(forms.ModelForm):
    class Meta:
        model = Chatbox
        fields = [
            'message', 'message_image'
        ]
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type a message...',
            }),
            'message_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }