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
    CooksListDelete,
    CooksListCreateView,
    CooksUpdateListView,
    IngredientsDishDeleteView, update_ingredients,

)

app_name = "core_app"

urlpatterns = [
    path("", index, name="index"),

    path("login/", login_view, name="login"),
    path("accounts/register/", register_user, name="register"),
    path("logout/", custom_logout, name="logout"),

    path("cooks/", CooksListView.as_view(), name="cooks-list"),
    path("cooks/delete/<int:pk>", CooksListDelete.as_view(),
         name="cooks-delete"),
    path("cooks/create/", CooksListCreateView.as_view(), name="cooks-create"),
    path("cooks/update/<int:pk>/", CooksUpdateListView.as_view(),
         name="cooks-update"),
    path("dishes/", DishesListView.as_view(), name="dishes-list"),
    path(
        "ingredients/<int:pk>/",
        IngredientsListView.as_view(),
        name="ingredients-list"
    ),
    path(
        "ingredients/dish/upgrade/<int:pk>/",
        update_ingredients,
        name="ingredient-dish-upgrade"
    ),
    path(
        "dish/<int:dish_pk>/ingredient/<int:pk>/delete/",
        IngredientsDishDeleteView.as_view(),
        name="ingredient-dish-delete"
    ),
    path("types-dish/", TypesDishListView.as_view(), name="types-dish"),
    path("types-dish/delete/<int:pk>/", TypeDishDeleteView.as_view(),
         name="type-dish-delete")

]
