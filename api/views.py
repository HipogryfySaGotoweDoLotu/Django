from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json

# Rejestracja
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    # templates are located in templates/api/, so use that path
    return render(request, 'api/register.html', {'form': form})

# Logowanie
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})

# Wylogowanie
def logout_view(request):
    logout(request)
    return redirect('login')

# Lista tasków
@login_required
def task_list(request):
    # legacy view: redirect to the card-style task list page
    return redirect('task_list')

# Dodawanie taska
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'api/task_form.html', {'form': form})

# Edycja taska
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            t = form.save(commit=False)
            t.edited = True
            t.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'api/task_form.html', {'form': form})


# Dashboard with calendar
@login_required
def dashboard(request):
    return render(request, 'api/dashboard.html')


@login_required
def panel(request):
    # main panel with tabs (calendar / task list)
    return render(request, 'api/panel.html')


@login_required
def task_list_page(request):
    # Dedicated Task List page (separate from calendar)
    return render(request, 'api/task_list_page.html')


@login_required
@require_GET
def api_task_list(request):
    qs = Task.objects.filter(user=request.user, in_calendar=False).order_by('-scheduled_date', 'scheduled_time')
    try:
        limit = int(request.GET.get('limit')) if request.GET.get('limit') else None
    except Exception:
        limit = None
    if limit:
        qs = qs[:limit]
    data = []
    for t in qs:
        data.append({
            'id': t.id,
            'name': t.name,
            'desc': t.desc,
            'scheduled_date': t.scheduled_date.isoformat() if t.scheduled_date else None,
            'scheduled_time': t.scheduled_time.isoformat() if t.scheduled_time else None,
            'priority': t.priority,
            'edited': t.edited,
            'completed': t.completed,  # ← DODAJ TO
        })
    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(['DELETE'])
def api_task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return JsonResponse({'ok': True})


@login_required
@require_GET
def calendar_events(request):
    # FullCalendar sends start/end as ISO dates
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = Task.objects.filter(user=request.user, scheduled_date__isnull=False, in_calendar=True)
    if start and end:
        qs = qs.filter(scheduled_date__gte=start, scheduled_date__lte=end)
    events = []
    for t in qs:
        start_dt = t.scheduled_date.isoformat()
        if t.scheduled_time:
            start_dt = f"{start_dt}T{t.scheduled_time.isoformat()}"
        events.append({
            'id': t.id,
            'title': t.name,
            'start': start_dt,
            'url': None,
            'editable': True,
            'priority': t.priority,
        })
    return JsonResponse(events, safe=False)


from datetime import datetime

@login_required
@require_POST
def api_create_task(request):
    # Accept JSON or form POST
    data = request.POST
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('invalid json')

    name = data.get('name')
    desc = data.get('desc', '')
    scheduled_date = data.get('scheduled_date')
    scheduled_time = data.get('scheduled_time')
    priority = data.get('priority') or Task.PRIORITY_MED
    in_calendar = data.get('in_calendar') in (True, 'true', 'True', '1', 1)

    if not name:
        return HttpResponseBadRequest('name required')

    task = Task(name=name, desc=desc, user=request.user)

    if scheduled_date:
        try:
            task.scheduled_date = datetime.strptime(scheduled_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest('invalid date format')
    if scheduled_time:
        try:
            task.scheduled_time = datetime.strptime(scheduled_time, "%H:%M").time()
        except ValueError:
            return HttpResponseBadRequest('invalid time format')

    task.priority = priority
    task.in_calendar = in_calendar
    task.save()
    return JsonResponse({
        'id': task.id,
        'name': task.name,
        'desc': task.desc,
        'scheduled_date': task.scheduled_date.isoformat() if task.scheduled_date else None,
        'scheduled_time': task.scheduled_time.isoformat() if task.scheduled_time else None,
        'priority': task.priority,
        'edited': task.edited,
        'completed': task.completed
    })


@login_required
@require_http_methods(["PATCH"])
def api_update_task_date(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('invalid json')
    # accept updates for scheduled_date, scheduled_time, priority, name, desc, in_calendar
    allowed = ('scheduled_date', 'scheduled_time', 'priority', 'name', 'desc', 'in_calendar')
    if not any(k in data for k in allowed):
        return HttpResponseBadRequest('no data')

    if 'scheduled_date' in data:
        task.scheduled_date = data.get('scheduled_date') or None
    if 'scheduled_time' in data:
        task.scheduled_time = data.get('scheduled_time') or None
    if 'priority' in data and data.get('priority'):
        task.priority = data.get('priority')
    if 'name' in data and data.get('name') is not None:
        task.name = data.get('name')
    if 'desc' in data:
        task.desc = data.get('desc') or ''
    if 'in_calendar' in data:
        # coerce several truthy values
        ival = data.get('in_calendar')
        task.in_calendar = True if ival in (True, 'true', 'True', '1', 1) else False

    task.edited = True
    task.save()
    return JsonResponse({'ok': True})
@login_required
@require_GET
def calendar_events(request):
    """
    Zwraca taski użytkownika dla FullCalendar z pełnym opisem i czasem.
    """
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = Task.objects.filter(user=request.user, scheduled_date__isnull=False, in_calendar=True)

    if start and end:
        qs = qs.filter(scheduled_date__gte=start, scheduled_date__lte=end)

    events = []
    for t in qs:
        start_dt = t.scheduled_date.isoformat()
        if t.scheduled_time:
            start_dt = f"{start_dt}T{t.scheduled_time.isoformat()}"
        events.append({
            'id': t.id,
            'title': t.name,
            'start': start_dt,
            'editable': True,
            'priority': t.priority,
            'desc': t.desc or '',
            'time': t.scheduled_time.isoformat() if t.scheduled_time else ''
        })
    return JsonResponse(events, safe=False)
@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def api_task_complete_toggle(request, pk):
    """
    Toggle task completed state via PATCH.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('invalid json')
    completed = data.get('completed')
    if completed is None:
        return HttpResponseBadRequest('completed field required')
    task.completed = bool(completed)
    task.save()
    return JsonResponse({'ok': True, 'completed': task.completed})
@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed=True).order_by('-scheduled_date', '-scheduled_time')
    return render(request, 'api/completed_tasks.html', {'tasks': tasks})
@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def api_task_complete_toggle(request, pk):
    """
    Toggle task completed state via PATCH.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('invalid json')

    completed = data.get('completed')
    if completed is None:
        return HttpResponseBadRequest('completed field required')

    task.completed = bool(completed)
    task.save()
    return JsonResponse({'ok': True, 'completed': task.completed})
