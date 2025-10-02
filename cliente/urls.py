from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.cliente_list, name='cliente_list'),
    path('cadastrar/', views.cliente_create, name='cliente_create'),
    path('editar/<int:id>/', views.cliente_update, name='cliente_update'),
    path('remover/<int:id>/', views.cliente_delete, name='cliente_delete'),
]
