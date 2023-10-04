from django.contrib import admin
from .models import Product, Lesson, Access, LessonWatched

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Access)
admin.site.register(LessonWatched)