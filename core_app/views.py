from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views import generic
from django.views.generic import ListView, View
from django.views.generic.edit import FormMixin, FormView
from django.contrib import messages

from core_app.forms import LoginForm, SignUpForm, DishTypeForm
from core_app.models import Cook, Dish, Ingredient, DishType


def index(request: HttpRequest) -> HttpResponse:
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_types_dishes = DishType.objects.count()

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_types": num_types_dishes,
    }
    return render(request, template_name="pages/index.html", context=context)


class CooksListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "pages/cook_list.html"
    paginate_by = 5


class CooksListDelete(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "pages/cooks_confirm_delete.html"
    success_url = reverse_lazy("core_app:cooks-list")


class CooksListCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "pages/cooks_create.html"
    fields = [
        "first_name",
        "last_name",
        "years_of_experience",
        "username",
    ]
    success_url = reverse_lazy("core_app:cooks-list")


class CooksUpdateListView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    template_name = "pages/cooks_create.html"
    fields = [
        "first_name",
        "last_name",
        "years_of_experience",
        "username",
    ]
    success_url = reverse_lazy("core_app:cooks-list")


class DishesListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "pages/dish_list.html"
    paginate_by = 4


class IngredientsListView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "pages/dish_ingredients_detail.html"


class UpgradeIngredientsView(LoginRequiredMixin, View):
    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        ingredient_name = request.POST.get("ingredient")
        if ingredient_name:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name
            )
            dish.ingredients.add(ingredient)

        return redirect("core_app:ingredients-list", pk=pk)


class IngredientsDishDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dish_pk = self.kwargs.get("dish_pk")
        ingredient_pk = self.kwargs.get("pk")

        dish = get_object_or_404(Dish, pk=dish_pk)
        ingredient = get_object_or_404(Ingredient, pk=ingredient_pk)

        return render(
            request,
            "pages/ingredient_confirm_delete.html",
            {"dish": dish, "ingredient": ingredient},
        )

    def post(self, request, *args, **kwargs):
        dish_pk = self.kwargs.get("dish_pk")
        ingredient_pk = self.kwargs.get("pk")
        dish = get_object_or_404(Dish, pk=dish_pk)
        ingredient = get_object_or_404(Ingredient, pk=ingredient_pk)
        dish.ingredients.remove(ingredient)
        return redirect("core_app:ingredients-list", pk=dish_pk)


class TypesDishListView(LoginRequiredMixin, FormMixin, ListView):
    model = DishType
    template_name = "pages/types_dish_list.html"
    paginate_by = 5
    form_class = DishTypeForm
    success_url = reverse_lazy("core_app:types-dish")
    success_message = "Added successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            form.success_message = self.success_message
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TypeDishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("core_app:types-dish")
    template_name = "pages/dishtype_confirm_delete.html"


class LoginUserView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form, msg="Invalid credentials"
                )
            )

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form, msg="Error validating the form"
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["msg"] = context.get("msg", None)
        return context


class RegisterUserView(FormView):
    template_name = "accounts/register.html"
    form_class = SignUpForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                msg="Form is invalid.",
                success=False
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["msg"] = context.get("msg", None)
        context["success"] = context.get("success", None)
        return context


class LogoutUserView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect("/")
