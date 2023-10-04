from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('lessons/', views.LessonListCreateAPIView.as_view(), name='lesson-list-create'), 
    path('lessons-watched/', views.LessonWatchedListCreateAPIView.as_view(), name='lesson-watched-list-create'), 
    path('access/', views.AccessListCreateAPIView.as_view(), name='access-list-create'),
    path('users/<int:user_id>/lessons/', views.UserLessonViewSet.as_view({'get': 'list'}), name='user-lessons-list'),  
    path('users/<int:user_id>/products/<int:product_id>/lessons/', views.ProductLessonsViewSet.as_view({'get': 'list'}), name='product-lessons-list'),
    path('product-statistics/', views.ProductStatisticsListAPIView.as_view(), name='product-statistics-list'),
   ]