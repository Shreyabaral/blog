from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import urls as auth_views

urlpatterns= [
#blog1

    path('contact/',views.contact,name='contact'),
    path('',views.aboutView.as_view(template_name="blog1/about.html"), name='about'),
    path('<slug:pk>/Detail/', views.PostDetailView.as_view(), name='post_detail'),
    path('ProfileDetail/', views.ProfileUpdate.as_view(), name='profile_detail'),
    path('<slug:pk>/Update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<slug:pk>/Delete/', views.PostDeleteView.as_view(), name='post_remove'),
    path('List/', views.PostListView.as_view(), name='post_list'),
    path('Create/', views.PostCreateView.as_view(), name='post_create'),
    path('Draft/', views.PostDraftView.as_view(), name='post_draft'),
    path('publish/', views.post_publish, name='post_publish'),
    path('<pk>/cadd/', views.add_comment_to_post, name='add_comment_to_post'),
    path('<int:pk>/capprove/', views.comment_approve, name='comment_approve'),
    path('<int:pk>/cremove/', views.comment_remove, name='comment_remove'),
    #path('accounts/login/', auth_views.views.auth_login,name='login'),
    #path('accounts/logout/', auth_views.views.auth_logout,name='logout'),
    path('login/',LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='registration/login.html'),name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
 ]
