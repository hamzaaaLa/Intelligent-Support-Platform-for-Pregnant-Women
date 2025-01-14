from django.urls import path
from . import views


urlpatterns =[
    path('',views.home,name="home"),
    path('inscription/',views.inscription,name="inscription"),
    path('connexion/',views.connexion,name="connexion"),
    path('risk/',views.risk,name="risk"),
    path('predict/', views.predictRisk, name='predictRisk'),
    path('logout/', views.logout_view, name='logout'),

]