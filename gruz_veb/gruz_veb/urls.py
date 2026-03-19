from django.contrib import admin
from django.urls import path
from gruz_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    # --- ТРАНСПОРТЫ ---
    path('admin-panel/transports/', admin_transport_list, name='admin_transport_list'),
    path('admin-panel/transports/create/', admin_transport_create, name='admin_transport_create'),
    path('admin-panel/transports/<int:pk>/edit/', admin_transport_edit, name='admin_transport_edit'),
    path('admin-panel/transports/<int:pk>/delete/', admin_transport_delete, name='admin_transport_delete'),

    # --- ТИПЫ ТРАНСПОРТА (Новое) ---
    path('admin-panel/transport-types/', admin_type_list, name='admin_type_list'),
    path('admin-panel/transport-types/create/', admin_type_create, name='admin_type_create'),
    path('admin-panel/transport-types/<int:pk>/edit/', admin_type_edit, name='admin_type_edit'),
    path('admin-panel/transport-types/<int:pk>/delete/', admin_type_delete, name='admin_type_delete'),


    path('admin-panel/users/', admin_user_list, name='admin_user_list'),
    path('admin-panel/users/create/', admin_user_create, name='admin_user_create'),
    path('admin-panel/users/<int:pk>/edit/', admin_user_edit, name='admin_user_edit'),
    path('admin-panel/users/<int:pk>/delete/', admin_user_delete, name='admin_user_delete'),


    path('admin-panel/roles/', admin_role_list, name='admin_role_list'),
    path('admin-panel/roles/create/', admin_role_create, name='admin_role_create'),
    path('admin-panel/roles/<int:pk>/edit/', admin_role_edit, name='admin_role_edit'),
    path('admin-panel/roles/<int:pk>/delete/', admin_role_delete, name='admin_role_delete'),


    # --- ГРУЗЫ (Новое) ---
    path('admin-panel/cargos/', admin_cargo_list, name='admin_cargo_list'),
    path('admin-panel/cargos/create/', admin_cargo_create, name='admin_cargo_create'),
    path('admin-panel/cargos/<int:pk>/edit/', admin_cargo_edit, name='admin_cargo_edit'),
    path('admin-panel/cargos/<int:pk>/delete/', admin_cargo_delete, name='admin_cargo_delete'),

    path('routes/', route_list, name='route_list'),
    path('routes/create/', route_create, name='route_create'),
    path('routes/<int:pk>/', route_detail, name='route_detail'),
    path('routes/<int:pk>/edit/', route_edit, name='route_edit'),
    path('routes/<int:pk>/delete/', route_delete, name='route_delete'),
]
