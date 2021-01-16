from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import Feedback, Comment
from django.views.generic import ( 
    CreateView, 
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
from .serializers import FeedbackSerializer, CommentSerializer, UserSerializer
###############################



def index(request: dict):
    '''Функция  index возвращает HTML главной страницы'''
    return render(
        request=request,
        template_name='main/index.html'
    )

def about(request: dict):
    '''Функция about возвращает страницу о компании.'''
    return render(
        request=request,
        template_name='main/about.html'
    )


def registration (request: str):
    '''Функция login возвращает страницу для регистрации'''
    if request.method == 'POST':
        regist_form = RegistrationForm(request.POST)
        if regist_form.is_valid():
            regist_form.save()
            return redirect('login')    
    else:
        regist_form = RegistrationForm()
        return render(
        request=request,
        template_name='main/registration.html',
        context={"regist_form": regist_form}
    )


# def feedback(request):
#     pass
#     feedback = Feedback.objects.all()
#     return render(
#         request=request,
#         template_name='main/feedbacks.html',
#         context={"feedback": feedback}
#     )


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    '''
    Класс для создания формы Отзыва
    '''
    model = Feedback
    fields = ('feedback_text',)
    template_name='main/feedback_create.html'

    # def get_context_data(self, **kwargs):
    #     kwargs["feedback"] = Feedback.objects.all()
    #     return super().get_context_data(**kwargs)


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class FeedbackListView(ListView):
    '''
    Класс для возвращения всех отзывов
    '''
    model = Feedback
    template_name='main/feedback_list.html'


class FeedbackDetailView(DetailView):
    '''
    Класс для возвращения определенного комментария из Отзывов
    '''
    model = Feedback
    template_name='main/feedback_details.html'

    def get_context_data(self, **kwargs):
        feedback = self.get_object()
        kwargs["comments"] = Comment.objects.filter(assigned_to_feedback=feedback.pk)
        return super().get_context_data(**kwargs)

class FeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    fields = ('feedback_text',)
    template_name = 'main/feedback_update.html'

    # def get_context_data(self, **kwargs):
    #     feedback = self.get_object()
    #     kwargs['feedback'] = Feedback.objects.get(pk=feedback.pk)
    #     kwargs['comments'] = Comment.objects.filter(assigned_to_feedback=feedback.pk)
    #     return super().get_context_data(**kwargs)


    def test_func(self):
        feedback = self.get_object()
        if self.request.user == feedback.author:
            return True
        return False
        


class FeedbackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feedback
    template_name='main/feedback_delete.html'
    success_url= '/feedback/list/'

    def test_func(self):
        feedback = self.get_object()
        if self.request.user == feedback.author:
            return True
        return False


######################################################################################################
#################################################### Django Rest Views ###################################################
######################################################################################################

class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = UserSerializer

    queryset = User.objects.all()
    
# class FeedbackListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     serializer_class = FeedbackSerializer
    
#     def get_queryset(self):
#         queryset = Feedback.objects.all()
#         return queryset
        

class FeedbackCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = FeedbackSerializer

    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = self.serializer_class(feedbacks, many=True)

        return Response(
            data={
                "success":True,
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
           

    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None

        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя нет в Базе Данных или Вы не указали author_id."
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


        serializer = FeedbackSerializer(
            data=request.data, 
            context={
                "author_id": author_id,
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Отзыв был оставлен успешно"
            },
            status=status.HTTP_201_CREATED
        )



class FeedbackUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer

    def put(self, request):
        try:
            feedback_id = Feedback.objects.get(pk=request.data.get('feedback_id'))

            serializer = FeedbackSerializer(
                instance=feedback_id,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success":True,
                    "result":"Отзыв был ОБНОВЛЁН успешно"
                },
                status=status.HTTP_200_OK
            )
        except Feedback.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


class FeedbackDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer

    def delete(self, request):
        try:
            feedback_id = Feedback.objects.get(pk=request.data.get('feedback_id'))
            feedback_id.delete()
            return Response(
                data={
                    "success":True,
                    "result":"Отзыв был УДАЛЁН успешно"
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Feedback.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def get(self, request):
        comment = Comment.objects.all()
        serializer = self.serializer_class(comment, many=True)

        return Response(
            data={
                "success":True,
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
           

    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None

        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя нет в Базе Данных или Вы не указали author_id."
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


        serializer = CommentSerializer(
            data=request.data, 
            context={
                "author_id": author_id,
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Комментарий был оставлен успешно"
            },
            status=status.HTTP_201_CREATED
        )


class CommentUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def put(self, request):
        try:
            comment_id = Comment.objects.get(pk=request.data.get('comment_id'))

            serializer = CommentSerializer(
                instance=comment_id,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success":True,
                    "result":"Комментарий был ОБНОВЛЁН успешно"
                },
                status=status.HTTP_200_OK
            )
        except Comment.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def delete(self, request):
        try:
            comment_id = Comment.objects.get(pk=request.data.get('comment_id'))
            comment_id.delete()
            return Response(
                data={
                    "success":True,
                    "result":"Комментарий был УДАЛЁН успешно"
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Comment.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Отзыв не найден!"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )