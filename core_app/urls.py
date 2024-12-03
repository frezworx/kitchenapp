from django.urls import path
from core_app.views import (
    index,
    login_view,
    register_user,
    custom_logout,
    CooksListView,
    DishesListView,
    IngredientsListView,
    TypesDishListView,
    TypeDishDeleteView,
)

app_name = "core_app"

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("accounts/register/", register_user, name="register"),
    path("logout/", custom_logout, name="logout"),

    path("cooks/", CooksListView.as_view(), name="cooks-list"),
    path("dishes/", DishesListView.as_view(), name="dishes-list"),
    path(
        "ingredients/<int:pk>/",
        IngredientsListView.as_view(),
        name="ingredients-list"
    ),
    path("types-dish/", TypesDishListView.as_view(), name="types-dish"),
    path("types-dish/delete/<int:pk>/", TypeDishDeleteView.as_view(),
         name="type-dish-delete")

]
