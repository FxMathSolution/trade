from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('api/', views.api, name='api'),
    path('add-account/', views.add_account, name='add_account'),
    path('modify-account/', views.modify_account, name='modify_account'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('get-accounts/', views.get_accounts, name='get_accounts'),
    path('get-orders/', views.get_orders, name='get_orders'),
    path('get-logs/', views.get_logs, name='get_logs'),
]