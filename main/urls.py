"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from agendadoce import views as agendadoce_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', agendadoce_views.login, name='login'),
    path('', agendadoce_views.index, name='index'),
    path('pedido/', agendadoce_views.pedido_list, name='pedido_list'),
    path('pedido/cadastrar', agendadoce_views.pedido_create, name='pedido_create'),
    path('pedido/editar/<int:id>/', agendadoce_views.pedido_update, name='pedido_update'),
    path('pedido/remover/<int:id>/', agendadoce_views.pedido_delete, name='pedido_delete'),
    path('pedido/<int:id>/', agendadoce_views.pedido_detail, name='pedido_detail'),
    path('cliente/', agendadoce_views.cliente_list, name='cliente_list'),
    path('cliente/cadastrar', agendadoce_views.cliente_create, name='cliente_create'),
    path('cliente/editar/<int:id>/', agendadoce_views.cliente_update, name='cliente_update'),
    path('cliente/remover/<int:id>/', agendadoce_views.cliente_delete, name='cliente_delete'),
    path('cliente/<int:id>/', agendadoce_views.cliente_detail, name='cliente_detail'),
    path('entregador/', agendadoce_views.entregador_list, name='entregador_list'),
    path('entregador/cadastrar', agendadoce_views.entregador_create, name='entregador_create'),
    path('entregador/editar/<int:id>/', agendadoce_views.entregador_update, name='entregador_update'),
    path('entregador/remover/<int:id>/', agendadoce_views.entregador_delete, name='entregador_delete'),
    path('entregador/<int:id>/', agendadoce_views.entregador_detail, name='entregador_detail'),
]
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
