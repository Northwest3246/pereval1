from django.urls import path
from . import views

app_name = 'passes'

urlpatterns = [
    path('submitData', views.submit_data, name='submit_data'),
    path('submitData/<int:pk>', views.get_pass, name='get_pass'),
    path('submitData/<int:pk>', views.edit_pass, name='edit_pass'),
    path('submitData/', views.get_passes_by_user, name='get_passes_by_user'),
]