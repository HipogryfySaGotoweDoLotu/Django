from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from api.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tasks/', include('api.urls')),  # wszystkie ścieżki z aplikacji api
    path('api/', RedirectView.as_view(pattern_name='task_list', permanent=False)),  # /api/ -> /tasks/
    path('api/task/<int:pk>/complete/', views.api_task_complete_toggle, name='api_task_complete_toggle'),

]
