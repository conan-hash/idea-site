"""
URL configuration for project_site project.

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
from authentication.views import * # Import views from the authentication app
from dashboard.views import * # Import views from the dashboard app
from django.conf import settings # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static


urlpatterns = [
    path('home/', home, name='home'),	 # Home page
	path('admin/', admin.site.urls),		 # Admin interface
	path('', user_login, name='login'), # Login page
    path('signup/', signup, name='signup'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('verification-sent/', TemplateView.as_view(template_name='verification_sent.html'), name='verification_sent'),
    path('verification-success/', TemplateView.as_view(template_name='verification_success.html'), name='verification_success'),
    path('home/user-profile/', user_profile, name='user_profile'),
	path('home/user-ideas/', user_ideas, name='user_ideas'), 
    path('home/ideas/', all_ideas, name='all_ideas'),
    path('home/track-idea/<str:identifier>/', track_idea, name='track_idea'),
    path('home/referee/', referee, name='referee'),
    path('logout/', user_logout, name='logout'),
    path('home/user-profile/', user_profile, name='user_profile'),
    #path('ideas/<int:pk>/', idea_detail, name='idea_detail'),
    path('home/successful/', successful, name='successful'),
    #path('ideas/<int:pk>/evaluate/', evaluate_idea, name='evaluate_idea'),
    #path('proposal/submit/', submit_proposal, name='submit_proposal'),
    #path('check-national-id/', check_national_id, name='check_national_id'),
    path('home/submit-new-idea/', submit_new_idea, name='submit_new_idea'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
