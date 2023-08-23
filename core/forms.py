from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction
from .models import Profile

User = get_user_model()

class RegisterForm(ModelForm):
    """
    The default 

    """
    
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control, fs-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control, fs-4'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'fs-4'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'fs-4'}))

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username=user.username.lower()
        user.set_password(self.cleaned_data["password1"])
        user.email = user.email.lower()

        if commit:
            user.save()
        return user

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_field_widgets()

    def _update_field_widgets(self):
        # Update the class attribute of each field's widget
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'bio',
            'location',
            'profileimg'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_field_widgets()

    def _update_field_widgets(self):
        # Update the class attribute of each field's widget
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})