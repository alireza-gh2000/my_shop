from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# ======= Login view =======
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("product_list")
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است")

    return render(request, "accounts/login.html")


# ======= Signup view =======
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1 or not password2:
            messages.error(request, "لطفاً تمام فیلدهای ضروری را پر کنید.")
            return render(request, "accounts/signup.html")

        if password1 != password2:
            messages.error(request, "رمز عبور یکسان نیست!")
            return render(request, "accounts/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً ثبت شده!")
            return render(request, "accounts/signup.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً ثبت شده!")
            return render(request, "accounts/signup.html")

        User.objects.create_user(username=username, email=email, password=password1)

        messages.success(request, "ثبت‌نام با موفقیت انجام شد! اکنون می‌توانید وارد شوید.")
        return redirect("auth")

    return render(request, "accounts/signup.html")


# ======= Combined auth (login + signup in one page) =======
def auth_view(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ---- Login ----
        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("product_list")

            messages.error(request, "نام کاربری یا رمز اشتباه است.")
            return redirect("auth")

        # ---- Signup ----
        if form_type == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "رمز عبور یکسان نیست!")
                return redirect("auth")

            if User.objects.filter(username=username).exists():
                messages.error(request, "نام کاربری تکراری است.")
                return redirect("auth")

            if email and User.objects.filter(email=email).exists():
                messages.error(request, "ایمیل تکراری است.")
                return redirect("auth")

            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد! حالا وارد شوید.")
            return redirect("auth")

    return render(request, "accounts/auth.html")


# ======= Logout =======
def logout_view(request):
    logout(request)
    return redirect("product_list")


# ======= Profile (protected) =======
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        user.save()
        messages.success(request, "پروفایل با موفقیت به‌روز شد.")
        return redirect("profile")

    return render(request, "accounts/edit_profile.html")
