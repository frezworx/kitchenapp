from django.contrib.auth import get_user_model

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
        self.assertTemplateUsed(response, "pages/index.html")

    def test_index_view_context_data(self):
        response = self.client.get(reverse("core_app:index"))
        self.assertIn("num_cooks", response.context)
        self.assertIn("num_dishes", response.context)
        self.assertIn("num_types", response.context)
        self.assertEqual(response.context["num_cooks"], 1)
        self.assertEqual(response.context["num_dishes"], 1)
        self.assertEqual(response.context["num_types"], 1)


class CooksListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("core_app:cooks-list")

    def test_lists_all_cooks(self):
        Cook.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        for i in range(13):
            Cook.objects.create(username=f"Cook{i}")

        response = self.client.get(f"{self.url}?page=3")
        self.assertEqual(response.status_code, 200)
        print(response.context["cook_list"])
        self.assertEqual(len(response.context["cook_list"]), 4)


class CooksUpdateListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.cook = Cook.objects.create_user(
            username='testuser',
            password='Secret123',
            first_name='John',
            last_name='Doe',
            years_of_experience=5
        )
        self.client.login(username='testuser', password='Secret123')

    def test_get_update_view(self):
        response = self.client.get(
            reverse('core_app:cooks-update', kwargs={'pk': self.cook.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/cooks_create.html')

    def test_post_update_view(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'years_of_experience': 10,
            'username': 'testuser'
        }
        response = self.client.post(
            reverse('core_app:cooks-update', kwargs={'pk': self.cook.pk}),
            data)
        self.assertEqual(response.status_code, 302)
        self.cook.refresh_from_db()
        self.assertEqual(self.cook.first_name, 'Jane')
        self.assertEqual(self.cook.last_name, 'Smith')
        self.assertEqual(self.cook.years_of_experience, 10)


class CooksListDeleteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cook = Cook.objects.create_user(
            username='testuser',
            password='Secret123',
            first_name='John',
            last_name='Doe',
            years_of_experience=5
        )

        self.test_del_cook = Cook.objects.create_user(
            username='testuser2',
            password='Secret123',
            first_name='John2',
            last_name='Doe2',
            years_of_experience=1
        )
        self.client.login(username='testuser', password='Secret123')

    def test_delete_cook(self):
        response = self.client.post(
            reverse('core_app:cooks-delete', args=[self.test_del_cook.id]),
        )
        print(f"Response status: {response.status_code}")
        print(f"Response URL: {response.url}")
        self.assertRedirects(response, reverse('core_app:cooks-list'))
        self.assertFalse(Cook.objects.filter(id=self.test_del_cook.id).exists())
