from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from api import views

urlpatterns = [
    path('', RedirectView.as_view(url='/tasks/panel/', permanent=False)),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='api/login.html'), name='login'),
    # use our simple logout view (accepts GET) to avoid 405 Method Not Allowed on GET
    path('logout/', views.logout_view, name='logout'),
    path('task/add/', views.task_create, name='task_create'),
    # include app urls under /tasks/ (so names like 'task_list' remain available)
    path('tasks/', include('api.urls')),
    # keep /api/ behavior: redirect to the named task_list view
    path('api/', RedirectView.as_view(pattern_name='task_list', permanent=False)),
    # i18n language switching
    path('i18n/', include('django.conf.urls.i18n')),
]
