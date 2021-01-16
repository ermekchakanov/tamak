from django.urls import path
from . import views
# from main import views as main_views


app_name = 'main'

urlpatterns = [
    path('main/', views.index, name='main'),
    # path('about/', views.AboutView.view_as(), name='about'),
    path('registration/', views.registration, name='registration'),
    
]
