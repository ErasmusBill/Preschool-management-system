from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.context_processors import request

from home_auth.models import CustomUser, PasswordResetRequest


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")  

       
        if not all([first_name, last_name, email, password, role]):
            messages.error(request, "All fields are required")
            return redirect("home_auth:register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("home_auth:register")

       
        user = CustomUser.objects.create_user(
            username=email,  
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role
        )

        auth_login(request, user)
        messages.success(request, "Signup successful!")

   
        if role == "admin":
            return redirect("school:dashboard")
        elif role == "student":
            return redirect("school:dashboard")
        elif role == "teacher":
            return redirect("school:dashboard")
        return redirect("school:index")

    return render(request, "authentication/register.html")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both fields are required")
            return redirect("home_auth:login")


        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")

  
            if user.role == "admin":
                return redirect("school:dashboard")
            elif user.role == "student":
                return redirect("school:dashboard")
            elif user.role == "teacher":
                return redirect("school:dashboard")
            else:
                return redirect("school:index")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home_auth:login")

    return render(request, "authentication/login.html")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is required")
            return redirect("home_auth:forgot-password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with this email")
            return redirect("home_auth:forgot-password")

        reset_request = PasswordResetRequest.objects.create(user=user)
        reset_request.send_reset_email()
        messages.success(request, "Password reset email sent")
        return redirect("home_auth:login")

    return render(request, "authentication/forgot-password.html")

def reset_password_view(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, "Invalid or expired token")
        return redirect("home_auth:forgot_password")

    if not reset_request.is_valid():
        messages.error(request, "Token has expired or already used")
        return redirect("home_auth:forgot-password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not new_password or not confirm_password:
            messages.error(request, "Both password fields are required")
            return redirect(f"/authentication/reset-password/{token}/")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(f"/authentication/reset-password/{token}/")

        user = reset_request.user
        user.set_password(new_password)
        user.save()

        reset_request.is_used = True
        reset_request.save()

        messages.success(request, "Password reset successful! You can now log in.")
        return redirect("home_auth:login")

    return render(request, "authentication/reset-password.html", {"token": token})


def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home_auth:login")

@login_required
def change_password(request, user_id):
    user: CustomUser = get_object_or_404(CustomUser, id=user_id)

   
    if request.user != user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:dashboard")

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("repeat_password")

        if not all([current_password, new_password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect("home_auth:change-password", user_id=user.id)

        if new_password != confirm_password:
            messages.error(request, "New password does not match with confirm password")
            return redirect("home_auth:change-password", user_id=user.id)

        if not user.check_password(current_password):
            messages.error(request, "You entered an incorrect current password")
            return redirect("home_auth:change-password", user_id=user.id)

        user.set_password(new_password)
        user.save()

        
        update_session_auth_hash(request, user)

        messages.success(request, "You have successfully changed your password")
        return redirect("school:dashboard")

    return render(request, "home_auth/change_password.html", {"user": user})