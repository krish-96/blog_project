from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, register_view, login_view, logout_view, contact_mail,
                    PostsList, post_view, create_post_view, post_update_view, post_delete_view,
                    AuthorsList, author_view, author_update_view, AuthorPostsList,
                    dashboard_view, profile_view, settings_view,
                    )

app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='blog/password_change_form.html'),
         name='password_change'
         ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'),
        name='password_change_done'
    ),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset_form.html'),
         name='reset_password'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='user-profile'),
    path('settings/', settings_view, name='user-settings'),
    path('my-posts/', AuthorPostsList.as_view(), name='my-posts'),

    path('posts/', PostsList.as_view(), name='posts'),
    path('post/<str:slug>/', post_view, name='post'),
    path('create-post', create_post_view, name='create-post'),
    path('delete-post/<str:slug>/', post_delete_view, name='delete-post'),
    path('update-post/<str:slug>/', post_update_view, name='update-post'),

    path('authors/', AuthorsList.as_view(), name='authors'),
    path('author/<str:slug>/', author_view, name='author'),
    path('update-author/<slug:slug>/', author_update_view, name='update-author'),

    path('contactus/', contact_mail, name='contactus'),

]
