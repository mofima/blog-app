from django import forms 
from django.contrib.auth.forms import AuthenticationForm

from .models import MyUser, Profile


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your first_name',
        'class': 'w-full py-4 px-6 rounded-xl'
    })) 

    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your last_name',
        'class': 'w-full py-4 px-6 rounded-xl'
    })) 

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    username = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = MyUser 
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already in use, please choose another.')
        return username 
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use, please choose another.')
        return email 
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password2']
    

class LoginForm(AuthenticationForm):
    username = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Input password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = MyUser
        fields = ['username', 'password']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your first_name',
        'class': 'w-full py-4 px-6 rounded-xl'
    })) 

    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your last_name',
        'class': 'w-full py-4 px-6 rounded-xl'
    })) 

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    username = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username']   


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)

    class Meta:
        model = Profile    
        fields = ['avatar', 'bio']

        
            