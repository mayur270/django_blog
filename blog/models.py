from django.db import models
from users.admin import CustomUser
from django.urls import reverse
from tinymce import HTMLField
from django.core.validators import RegexValidator

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

def author_profile(user):
    author = Author.objects.get_or_create(user=user)
    return author

CustomUser.author = property(author_profile)

class Category(models.Model):
    title = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='media/images/')
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    content = HTMLField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_single', kwargs={
            'id':self.id
        })

    def get_update_url(self):
        return reverse('blog_update', kwargs={
            'id':self.id
        })

    def get_delete_url(self):
        return reverse('blog_delete', kwargs={
            'id':self.id
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
        
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
