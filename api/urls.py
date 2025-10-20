from django.urls import path
from . import views

urlpatterns = [
    # Show the card-style Task List at /tasks/ (replaces old list view)
    path('', views.task_list_page, name='task_list'),
    path('task/add/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('panel/', views.panel, name='panel'),
    path('list/', views.task_list_page, name='task_list_page'),
    # API for calendar
    path('api/calendar/', views.calendar_events, name='api_calendar'),
    path('api/create/', views.api_create_task, name='api_create_task'),
    path('api/<int:pk>/date/', views.api_update_task_date, name='api_update_task_date'),
    path('api/list/', views.api_task_list, name='api_task_list'),
    path('api/<int:pk>/delete/', views.api_task_delete, name='api_task_delete'),
    path('api/task/<int:pk>/complete/', views.api_task_complete_toggle, name='api_task_complete_toggle'),
    path('completed/', views.completed_tasks, name='completed_tasks'),


]
