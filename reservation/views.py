from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib.auth.models import User
from .models import Order
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    ListView
)


#################################
########### Rest Imports #############
#################################
from rest_framework import generics,status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, User
from rest_framework import serializers
from .serializers import OrderSerializer
###############################


# @login_required
# def reservation(request):
#     '''Данная функция обратывает данные с формы бронирования.
#     Если бронь успешна, отправляем пользователя на главную,
#     иначе просим перезаполнить. 
#     '''
#     book_form = ReservationForm()
#     if request.method == 'POST':
#         book_form = ReservationForm(request.POST)
#         if book_form.is_valid():
#             book_form = book_form.save(commit=False)
#             book_form.reservator = request.user
#             book_form.save()

#             return redirect('main:main')
            
#         return render(
#             request=request,
#             template_name='reservation/reservation.html',
#             context={"book_form": book_form}
#         )
    
#     return render(
#             request=request,
#             template_name='reservation/reservation.html',
#             context={"book_form": book_form}
#         )

class OrderCreateView(CreateView):
    '''
    Класс для создания формы бронирования
    '''
    model = Order
    fields = ('phone', 'date', 'time', 'persons', 'message',)
    template_name='reservation/reservation.html'

    def form_valid(self, form):
        form.instance.reservator = self.request.user
        return super().form_valid(form)

# def user_orders(request):
#     '''Функция возвращает список заказов пользователя.'''
#     user_list_orders = Order.objects.filter(reservator=request.user)
#     return render(
#         request=request,
#         template_name='reservation/user_orders.html',
#         context={"user_list_orders": user_list_orders}
#     )

class UserordersListView(ListView):
    '''
    Класс для возвращения списка броней
    '''
    model = Order
    template_name='reservation/user_orders.html'

    def get_context_data(self, **kwargs):
        kwargs["user_list_orders"] = Order.objects.filter(reservator=self.request.user)
        return super().get_context_data(**kwargs)

######################################################################################################
#################################################### Django Rest Views ###################################################
######################################################################################################

class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = UserSerializer

    queryset = User.objects.all()


class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(orders, many=True)

        return Response(
            data={
                "success":True,
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
           

    def post(self, request):
        try:
            if request.data.get('reservator_id'):
                user = User.objects.get(pk=request.data.get('reservator_id'))
                reservator_id = user.pk
            else:
                reservator_id = None

        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя нет в Базе Данных или Вы не указали author_id."
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


        serializer = OrderSerializer(
            data=request.data, 
            context={
                "reservator_id": reservator_id,
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Ваш заказ успешно забронирован"
            },
            status=status.HTTP_201_CREATED
        )



class OrderUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer

    def put(self, request):
        try:
            reservator_id = Order.objects.get(pk=request.data.get('reservator_id'))

            serializer = OrderSerializer(
                instance=reservator_id,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success":True,
                    "result":"Заказ был ОБНОВЛЁН успешно"
                },
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


class OrderDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer

    def delete(self, request):
        try:
            reservator_id = Order.objects.get(pk=request.data.get('reservator_id'))
            reservator_id.delete()
            return Response(
                data={
                    "success":True,
                    "result":"Заказ был УДАЛЁН успешно"
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Order.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )