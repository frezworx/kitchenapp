from core_app.models import Cook, Dish, DishType
from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        Cook.objects.create(username="Test Cook")
        Dish.objects.create(name="Test Dish", price=10.00)
        DishType.objects.create(name="Test Dish Type")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("core_app:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse("core_app:index"))
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_index_view_context_data(self):
        response = self.client.get(reverse("core_app:index"))
        self.assertIn("num_cooks", response.context)
        self.assertIn("num_dishes", response.context)
        self.assertIn("num_types", response.context)
        self.assertEqual(response.context["num_cooks"], 1)
        self.assertEqual(response.context["num_dishes"], 1)
        self.assertEqual(response.context["num_types"], 1)
