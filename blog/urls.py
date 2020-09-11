from django.urls import path, include
from .views import (blog_home, blog_about, blog_contact, blog_search, blog_single, blog_create, blog_update, blog_delete, contact_confirmation)

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('about/', blog_about, name='blog_about'),
    path('contact/', blog_contact, name='blog_contact'),
    path('search/', blog_search, name='blog_search'),
    path('single_post/<int:id>', blog_single, name='blog_single'),
    path('create/', blog_create, name='blog_create'),
    path('update/<int:id>/', blog_update, name='blog_update'),
    path('delete/<int:id>/', blog_delete, name='blog_delete'),
    path('contact_confirmation/', contact_confirmation, name='contact_confirmation'),
    path('text-editor/', include('tinymce.urls')),
]
