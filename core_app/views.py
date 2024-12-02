from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from core_app.forms import LoginForm, SignUpForm
from core_app.models import Cook, Dish, Ingredient, DishType


def index(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="pages/index.html")


class CooksListView(generic.ListView):
    model = Cook
    template_name = "pages/cook_list.html"
    paginate_by = 5


class DishesListView(generic.ListView):
    model = Dish
    template_name = "pages/dish_list.html"
    paginate_by = 4


class IngredientsListView(generic.ListView):
    model = Ingredient
    template_name = "pages/ingredient_list.html"


class TypesDishListView(generic.ListView):
    model = DishType
    template_name = "pages/types_dish_list.html"


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(
        request,
        "accounts/login.html",
        {"form": form, "msg": msg}
    )


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success}
    )


def custom_logout(request: HttpRequest):
    logout(request)
    return redirect("/")
