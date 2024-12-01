from django.urls import path
from core_app.views import index

urlpatterns = [
    path("", index, name="index"),
]
