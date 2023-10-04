from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Product, Lesson, Access, LessonWatched

class TestAPIViews(TestCase):
    def setUp(self):
        # Initialize the test client and create a user for testing
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')

    def test_user_list_create_view(self):
        # Test the user list create view
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_lesson_view(self):
        # Test the user lessons list view
        url = reverse('user-lessons-list', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_list_create_view(self):
        url = reverse('product-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_list_create_view(self):
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_watched_list_create_view(self):
        url = reverse('lesson-watched-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_access_list_create_view(self):
        url = reverse('access-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_statistics_view(self):
        # Test the products statistics list view
        url = reverse('product-statistics-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class TestProductLessonsViewSet(TestCase):
    # Initialize the test client and create necessary objects for testing   
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.product  = Product.objects.create(name='Test Product', owner=self.user)
        self.access = Access.objects.create(product=self.product)
        self.access.users.add(self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', duration_seconds=1000)
        self.lesson.products.set([self.product]) 
        self.lesson_watched = LessonWatched.objects.create(user=self.user, lesson=self.lesson)

    def test_product_lessons_view(self):
        # Test the product lessons view with access
        url = reverse('product-lessons-list', args=[self.user.id, self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_lessons_view_without_access(self):
        # Test the product lessons view without access
        new_user = User.objects.create(username='newuser')
        url = reverse('product-lessons-list', args=[new_user.id, self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    
