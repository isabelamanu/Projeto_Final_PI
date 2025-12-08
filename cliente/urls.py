from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"), # p/ usu visualizar
    path("historico/", views.historico_cliente, name="historico"),
    path("", views.cliente_list, name="cliente_list"),
    path("cadastrar/", views.cliente_create, name="cliente_create"),  # p/ cadastro próprio
    path("editar/<int:id>/", views.cliente_update, name="cliente_update"),  # p/ usu editar próprio perfil
    path("remover/<int:id>/", views.cliente_delete, name="cliente_delete"), 
    path("detail/<int:id>/", views.cliente_detail, name="cliente_detail"),  # p/ admin visualizar
    path("gerenciar/criar/", views.create_usuario_admin, name="create_usuario_admin"),  # para admin criar usu pelo sistema
    path("gerenciar/editar/<int:id>/", views.update_usuario_admin, name="update_usuario_admin"),  # para admin editar usu
]
