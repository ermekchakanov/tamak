from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import Chief
from django.views.generic import ( 
    CreateView,
    ListView,
)

class ChiefCreateView(CreateView):
    '''
    Класс для создания формы добавления персонала
    '''
    model = Chief
    fields = '__all__'
    template_name = 'teams/teams.html'

    def get_context_data(self, **kwargs):
        kwargs["chief"] = Chief.objects.all()
        return super().get_context_data(**kwargs)



# class ChiefListView(ListView):
#     model = Chief
#     fields = '__all__'
#     template_name = 'teams/teams.html'


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
from .serializers import ChiefSerializer
########################################
########################################
########################################


######################################################################################################
#################################################### Django Rest Views ###################################################
######################################################################################################

class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = UserSerializer

    queryset = User.objects.all()


class ChiefCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ChiefSerializer

    def get(self, request):
        chiefs = Chief.objects.all()
        serializer = self.serializer_class(chiefs, many=True)

        return Response(
            data={
                "success":True,
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
           

    def post(self, request):
        try:
            if request.data.get('user_id'):
                user = User.objects.get(pk=request.data.get('user_id'))
                user_id = user.pk
            else:
                user_id = None

        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя нет в Базе Данных или Вы не указали author_id."
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


        serializer = ChiefSerializer(
            data=request.data, 
            context={
                "user_id": user_id,
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Персонал успешно добавлен"
            },
            status=status.HTTP_201_CREATED
        )



class ChiefUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChiefSerializer

    def put(self, request):
        try:
            user_id = Chief.objects.get(pk=request.data.get('user_id'))

            serializer = ChiefSerializer(
                instance=user_id,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success":True,
                    "result":"Персонал был ОБНОВЛЁН успешно"
                },
                status=status.HTTP_200_OK
            )
        except Chief.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Персонал не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


# class OrderDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = OrderSerializer

#     def delete(self, request):
#         try:
#             reservator_id = Order.objects.get(pk=request.data.get('reservator_id'))
#             reservator_id.delete()
#             return Response(
#                 data={
#                     "success":True,
#                     "result":"Заказ был УДАЛЁН успешно"
#                 },
#                 status=status.HTTP_202_ACCEPTED
#             )
#         except Order.DoesNotExist:
#             return Response(
#             data={
#                 "success":False,
#                 "result":"Отзыв не найден!"
#             },
#             status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
#         )


