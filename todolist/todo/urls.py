from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
    path('csrf-test/', views.csrf_test, name='csrf_test'),
    path('csrf-exempt-test/', views.csrf_exempt_test, name='csrf_exempt_test'),
    path('js-form-test/', views.js_form_test, name='js_form_test'),
]
