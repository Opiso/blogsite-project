"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='blog-index'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('feedbacks/', views.feedbacks, name='blog-feedbacks'),
    path('search/', views.search_view, name='blog-search'),
    path('post/delete/<int:id>/', views.delete_blog_post, name='blog-delete'),
    path('post/update/<int:id>/', views.update_blog_post, name='blog-update'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/<int:id>/comment/<int:comment_id>/delete/', views.delete_comment, name='comment-delete'),
    path('feedbacks/delete/<int:feedback_id>/', views.admin_delete_feedback, name='feedback-delete'),
    path('feedbacks/approve/<int:feedback_id>/', views.approve_feedback, name='feedback-approve'),

]

