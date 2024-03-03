from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views import View 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView

from .models import MyUser
from .forms import SignupForm, UpdateProfileForm, UpdateUserForm 
from .token import account_activation_token 

class SignupView(View):
    template = 'account/signup.html'

    def get(self, request):
        form = SignupForm()
        ctx = {'form': form}

        return render(request, self.template, ctx)
    
    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False 
            user.save()

            # EMAIL SETUP
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER)
            messages.success(request, 'Registered successfully and activation link sent to provided email.')
            return redirect('item:index')
    
        else:
            return render(request, 'account/signup.html', {'form': form})       


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None 
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True 
        user.save()

        login(request, user)
        return redirect('item:index')
    else:
        return render(request, 'account/activation_invalid.html')   
    

class Profile(View, LoginRequiredMixin):

    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        ctx = {'user_form': user_form,
               'profile_form': profile_form}
        return render(request, 'account/profile.html', ctx)
    
    def post(self, request):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, 
                                         request.FILES, 
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('account:profile')    


class ResetPasswordView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    # when using name spaced url, ensure to use reverse_lazy('app_name: urlname') not reverse_lazy('urlname')
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder.")
        return response 
    
class ResetConfirmPassword(PasswordResetConfirmView):
    template_name='account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')     


class ChangePasswordView(PasswordChangeView):
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('account:profile')   

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Successfully Changed Your Password")
        return response

