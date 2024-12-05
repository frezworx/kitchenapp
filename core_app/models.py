from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CASCADE


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username} ({self.last_name}, {self.first_name})"


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    type_dish = models.ForeignKey(DishType, on_delete=CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="prepared_dishes")
    ingredients = models.ManyToManyField(
        Ingredient, related_name="included_in_dishes"
    )

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return (
            f"{self.name} - "
            f"{self.type_dish.name if self.type_dish else 'No Type'}, "
            f"{self.price}"
        )
