from django.db import models
from django.contrib.auth.models import User

# Model representing a Product with a name and an owner (ForeignKey to User)
class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Model representing Access, linking multiple users to a product
class Access(models.Model):
    users = models.ManyToManyField(User)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        usernames = ', '.join(user.username for user in self.users.all())
        return f"{usernames} - {self.product.name}"

# Model representing a Lesson with a name, video link, duration, and related products
class Lesson(models.Model):
    name = models.CharField(max_length=100)
    video_link = models.URLField()
    duration_seconds = models.IntegerField(null=True, blank=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

# Model representing a Lesson being watched by a user
class LessonWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_time_seconds = models.IntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    last_watched_time = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if user has access to the associated product of the lesson
        access = Access.objects.filter(users=self.user, product=self.lesson.products.first()).exists()
        
        if access:
            if self.lesson.duration_seconds is not None and self.watched_time_seconds is not None:
                # Check if 80% of the lesson is watched
                if (self.watched_time_seconds / self.lesson.duration_seconds) >= 0.8:
                    self.is_completed = True
            
            super().save(*args, **kwargs)
            

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name}"