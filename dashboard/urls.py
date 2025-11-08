from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('encrypt/<int:file_id>/', views.encrypt_file_view, name='encrypt_file'),
    path('decrypt/<int:file_id>/', views.decrypt_file_view, name='decrypt_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('scan/<int:file_id>/', views.scan_file_view, name='scan_file'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
