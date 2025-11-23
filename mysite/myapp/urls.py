from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('students/', views.students, name='students'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edits, name='edit_student'),
    path('dels/<int:id>/', views.dels, name='dels'),
    path('add/', views.add, name='add'),
    path('otp/', views.otp_v, name='otp'),
    path('login/', views.login, name='login'),
    path('log_in/', views.log_in, name='log_in'),
    path('logout/', views.logout, name='logout'),
    path('dash/', views.dash, name='dash'),
    path('chat/', views.chat, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('clear/', views.clear, name='clear'),
    path('delete-friend/', views.delete_friend, name='delete_friend'),
    
]