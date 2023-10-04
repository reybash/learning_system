from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .serializers import (
    LessonWatchedSerializer,
    LessonSerializer,
    ProductSerializer,
    AccessSerializer,
    ProductStatisticsSerializer,
    UserLessonSerializer,
    ProductLessonSerializer,
    UserSerializer,
)
from .models import Product, Lesson, Access, LessonWatched

def index(request):
    return HttpResponse("Hello, world. This is testing API.")

class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing or creating products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing or creating lessons.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    
class LessonWatchedListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing or creating watched lessons.
    """
    queryset = LessonWatched.objects.all()
    serializer_class = LessonWatchedSerializer
    
class AccessListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing or creating accesses.
    """
    queryset = Access.objects.all()
    serializer_class = AccessSerializer

class UserLessonViewSet(viewsets.ViewSet):
    """
    API endpoint for listing user's lessons.
    """
    serializer_class = UserLessonSerializer

    def list(self, request, user_id):
        # Checking user's access to the lessons
        if not Access.objects.filter(users=user_id).exists():
            return Response([])  # Return an empty list if user has no access
        
        # Get all lessons
        products = Access.objects.filter(users=user_id).values_list('product__id', flat=True)
        lessons = Lesson.objects.filter(products__in=products).distinct()
        lessons_watched = LessonWatched.objects.filter(user=user_id)
        
        lesson_serializer = UserLessonSerializer(lessons, context={'lessons_watched': lessons_watched}, many=True)

        return Response(lesson_serializer.data)
    
class ProductLessonsViewSet(viewsets.ViewSet):
    """
    API endpoint for listing product's lessons for user.
    """
    serializer_class = ProductLessonSerializer

    def list(self, request, user_id,product_id):
        # Checking user's access to the product
        if not Access.objects.filter(users=user_id, product_id=product_id).exists():
           return Response([])  # Return an empty list if user has no access
        
        # Get all lessons associated with the product
        lessons = Lesson.objects.filter(products=product_id)
        lessons_watched = LessonWatched.objects.filter(user=user_id)
       
        lesson_serializer = ProductLessonSerializer(lessons, context={'lessons_watched': lessons_watched}, many=True)

        return Response(lesson_serializer.data)

class ProductStatisticsListAPIView(generics.ListAPIView):
    """
    API endpoint for product statistics.
    """
    serializer_class = ProductStatisticsSerializer

    def get_queryset(self):
        return Product.objects.all()