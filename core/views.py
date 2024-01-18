from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm, UserForm


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

    else:
        profile_form = ProfileForm(instance=request.user)
        user_form = UserForm()

    password_form = PasswordForm(user=request.user)
    return render(request, 'user/profile.html',{
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form':password_form,
            'profile_tab': True
           })

@login_required
def profile_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('edit_user_profile')

    else:
        password_form = PasswordForm(user=request.user)

    profile_form = ProfileForm(instance=request.user)
    user_form = UserForm()
    return render(request, 'user/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form':password_form,
            'password_tab':True
            })