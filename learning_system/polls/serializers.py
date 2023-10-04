from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Product, Lesson, Access, LessonWatched

# Serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        lookup_field = 'username' 
        
class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'owner']
        
class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_link', 'duration_seconds', 'products']

class LessonWatchedSerializer(serializers.ModelSerializer):
    """
    Serializer for the LessonWatched model.
    """
    lesson = LessonSerializer()
    class Meta:
        model = LessonWatched
        fields = ['lesson', 'watched_time_seconds', 'is_completed', 'last_watched_time']

class AccessSerializer(serializers.ModelSerializer):
    """
    Serializer for the Access model.
    """
    class Meta:
        model = Access
        fields = ['id', 'users', 'product']

class UserLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for user lessons.
    """
    watched_time_seconds = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_link', 'duration_seconds', 'watched_time_seconds', 'is_completed']

    def get_watched_time_seconds(self, obj):
        # Assuming lessons_watched is a list of LessonWatched objects
        lessons_watched = self.context.get('lessons_watched', [])
        lesson_id = getattr(obj, 'id', None)  # Using getattr to avoid exceptions
        return self._get_value_from_lessons_watched(lessons_watched, lesson_id, 'watched_time_seconds')

    def get_is_completed(self, obj):
        # Similar to is_completed
        lessons_watched = self.context.get('lessons_watched', [])
        lesson_id = getattr(obj, 'id', None)
        return self._get_value_from_lessons_watched(lessons_watched, lesson_id, 'is_completed')
    
    def _get_value_from_lessons_watched(self, lessons_watched, lesson_id, field):
        # Find the LessonWatched object with the matching lesson_id
        for lw in lessons_watched:
            if lw.lesson.id == lesson_id:
                return getattr(lw, field)
        return None  # Return None instead of False depending on the logic.

    
class ProductLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for user product lessons.
    """
    watched_time_seconds = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    last_watched_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_link', 'duration_seconds', 'watched_time_seconds', 'is_completed', 'last_watched_time']

    def get_watched_time_seconds(self, obj):
        # Assuming lessons_watched is a list of LessonWatched objects
        lessons_watched = self.context.get('lessons_watched', [])
        lesson_id = getattr(obj, 'id', None)  # Using getattr to avoid exceptions
        return self._get_value_from_lessons_watched(lessons_watched, lesson_id, 'watched_time_seconds')
        
    def get_is_completed(self, obj):
        # Similar to get_watched_time_seconds
        lessons_watched = self.context.get('lessons_watched', [])
        lesson_id = getattr(obj, 'id', None)  
        return self._get_value_from_lessons_watched(lessons_watched, lesson_id, 'is_completed')
    
    def get_last_watched_time(self, obj):
        lessons_watched = self.context.get('lessons_watched', [])
        lesson_id = getattr(obj, 'id', None)  
        return self._get_value_from_lessons_watched(lessons_watched, lesson_id, 'last_watched_time')
    
    def _get_value_from_lessons_watched(self, lessons_watched, lesson_id, field):
        # Find the LessonWatched object with the matching lesson_id
        for lw in lessons_watched:
            if lw.lesson.id == lesson_id:
                return getattr(lw, field)
        return None  # Return None instead of False depending on the logic.

class ProductStatisticsSerializer(serializers.ModelSerializer):
    """
    Serializer for product statistics.
    """
    total_lessons_watched = serializers.SerializerMethodField()
    total_watch_time_seconds = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'total_watch_time_seconds', 'total_lessons_watched', 'total_users', 'purchase_percentage']
    
    def get_total_lessons_watched(self, obj):
        return LessonWatched.objects.filter(lesson__products=obj).count()

    def get_total_watch_time_seconds(self, obj):
        total_watch_time = LessonWatched.objects.filter(lesson__products=obj).aggregate(total_watch_time=Sum('watched_time_seconds'))
        return total_watch_time['total_watch_time'] or 0

    def get_total_users(self, obj):
        return Access.objects.filter(product=obj).values('users').count()

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        product_users = Access.objects.filter(product=obj).values('users').count()
        return (product_users / total_users) * 100 if total_users > 0 else 0