from django.contrib import admin

# Register your models here.
from .models import Post, Category, Author, Comment, Contact

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
