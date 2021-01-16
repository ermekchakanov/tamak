"""tamak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main import views as main_views
from reservation import views as reservation_views
from teams import views as teams_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('reservation/', include ('reservation.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='Logout'),
    path('registration/', main_views.registration, name='registration'),
    path('feedback/create/', main_views.FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/list/', main_views.FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/detail/<int:pk>/', main_views.FeedbackDetailView.as_view(), name='feedback-details'),    
    path('feedback/update/<int:pk>/', main_views.FeedbackUpdateView.as_view(), name='feedback-update'),
    path('feedback/delete/<int:pk>/', main_views.FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('teams/', include('teams.urls')),

    ###########################################################################################################################

    path('api-auth/', include ('rest_framework.urls')),
    path('api/v1/get_all_user/', main_views.UserListAPIView.as_view(), name='get-all-users-api'),
    path('api/v1/all_feedbacks/', main_views.FeedbackCreateAPIView.as_view(), name='all-feedbacks-api'),
    path('api/v1/all_comments/', main_views.CommentCreateAPIView.as_view(), name='all-comments-api'),
    path('api/v1/all_comments_update/', main_views.CommentUpdateAPIView.as_view(), name='all-comments-update-api'),
    path('api/v1/all_comments_delete/', main_views.CommentDeleteAPIView.as_view(), name='all-comments-delete-api'),
    path('api/v1/all_orders/', reservation_views.OrderCreateAPIView.as_view(), name='all-orders-api'),
    path('api/v1/all_orders_update/', reservation_views.OrderUpdateAPIView.as_view(), name='all-orders-update-api'),
    path('api/v1/all_orders_delete/', reservation_views.OrderDeleteAPIView.as_view(), name='all-orders-delete-api'),
    path('api/v1/all_chiefs/', teams_views.ChiefCreateAPIView.as_view(), name='all-chiefs-api'),
    path('api/v1/all_chiefs_update/', teams_views.ChiefUpdateAPIView.as_view(), name='all-chiefs-update-api'),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)