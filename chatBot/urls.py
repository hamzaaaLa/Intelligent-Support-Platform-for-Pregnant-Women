from django.urls import path
from . import views


urlpatterns =[
    path('',views.chatPage, name="chatBot"),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
]