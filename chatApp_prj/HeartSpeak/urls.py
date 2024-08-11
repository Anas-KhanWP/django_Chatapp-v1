from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('', views.default_chat_view, name='default_chat_view'),
    path('<int:recipient_id>/', views.chat_view, name='chat_view'),
]
