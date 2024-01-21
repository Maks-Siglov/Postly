from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from users.models import User
from users.services.verification_email import send_verification_email
from users.forms import RegisterForm, LoginForm, ResetPasswordEmailForm


def registration(request) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            send_verification_email(
                request,
                user,
                subject="Registration Confirmation",
                template='users/emails/account_verification_email.html',
            )
            return render(request, "users/registration_success.html")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile:profile", user.username)

            form.add_error(None, "Invalid login credentials")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def forgot_password(request) -> HttpResponse:
    if request.method == "POST":
        form = ResetPasswordEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)

            send_verification_email(
                request,
                user,
                subject="Reset Your Password",
                template='users/emails/reset_password_email.html',
            )
            messages.success(
                request,
                'Your password reset link has been sent'
                ' to your email address.'
            )
            return redirect('users:login')

        else:
            messages.warning(request, 'Account with this email does not exist')
            return redirect('users:forgot_password')

    else:
        form = ResetPasswordEmailForm()
    return render(request, "users/forgot_password.html", {"form": form})


def reset_password_validation(
        request, uidb64: str, token: str
) -> HttpResponseRedirect:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, 'Please resset your password')
        return redirect('users:reset_password')

    else:
        messages.error(request, 'This link is invalid or expired.')
        return redirect('users:login')


def reset_password(request) -> HttpResponse | HttpResponseRedirect:
    pk = request.session.get("uid")
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        form = SetPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save(user)
            messages.success(request, 'You successfully reset your password.')
            return redirect('users:login')
    else:
        form = SetPasswordForm(request.user)
    return render(
        request, 'users/reset_password.html', {"form": form}
    )
