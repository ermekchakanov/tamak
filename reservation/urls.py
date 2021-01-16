from django.urls import path
from . import views



app_name = 'reservation'


urlpatterns = [
    path('', views.OrderCreateView.as_view(), name='reservation'),
    path('my_reservations/', views.UserordersListView.as_view(), name='my_reservations'),
]
