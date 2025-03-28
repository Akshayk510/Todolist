from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Task
from django.contrib import messages
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# User Authentication Views
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validate form data
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup.html')

        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Task Management Views
@login_required
def task_list(request):
    from datetime import datetime
    import logging
    from django.db import OperationalError

    logger = logging.getLogger(__name__)

    # Get filter parameters from request
    filter_status = request.GET.get('status', 'all')
    filter_priority = request.GET.get('priority', 'all')
    filter_category = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', '-created_at')

    # Check if sort_by is a valid field
    valid_sort_fields = ['-created_at', 'created_at', 'title', '-title']
    if sort_by not in valid_sort_fields:
        sort_by = '-created_at'

    try:
        # Base queryset
        tasks = Task.objects.filter(user=request.user)

        # Apply filters
        if filter_status == 'completed':
            tasks = tasks.filter(completed=True)
        elif filter_status == 'active':
            tasks = tasks.filter(completed=False)

        # Try to apply priority filter if the field exists
        try:
            if filter_priority != 'all':
                tasks = tasks.filter(priority=filter_priority)
        except OperationalError as e:
            if 'no such column: todo_task.priority' in str(e):
                logger.warning("Priority column doesn't exist yet. Skipping priority filter.")
                filter_priority = 'all'
            else:
                raise

        # Try to apply category filter if the field exists
        try:
            if filter_category != 'all':
                tasks = tasks.filter(category=filter_category)
        except OperationalError as e:
            if 'no such column: todo_task.category' in str(e):
                logger.warning("Category column doesn't exist yet. Skipping category filter.")
                filter_category = 'all'
            else:
                raise

        # Apply sorting
        try:
            tasks = tasks.order_by(sort_by)
        except OperationalError:
            # If sorting by a non-existent field, use created_at
            tasks = tasks.order_by('-created_at')
    except Exception as e:
        # If there's an error, set tasks to an empty list
        logger.error(f"Error fetching tasks: {e}")
        tasks = []

    # Prepare context
    context = {
        'tasks': tasks,
        'now': datetime.now(),
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'filter_category': filter_category,
        'sort_by': sort_by,
        'categories': Task.CATEGORY_CHOICES,
        'priorities': Task.PRIORITY_CHOICES
    }

    return render(request, 'task_list.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            description = request.POST.get('description', '')
            deadline = request.POST.get('deadline', None)
            category = request.POST.get('category', 'other')
            priority = request.POST.get('priority', 'medium')
            if not title.strip():
                messages.error(request, "Task title cannot be empty!")
                return render(request, 'add_task.html')
            # Create the task with the provided information
            task = Task.objects.create(
                title=title,
                description=description,
                user=request.user,
                deadline=deadline,
                category=category,
                priority=priority
            )
            messages.success(request, "Task added successfully!")
            return redirect('task_list')
        except Exception as e:
            messages.error(request, f"Error creating task: {str(e)}")
            return render(request, 'add_task.html')
    
    # Get categories and priorities from model choices for the template
    context = {
        'categories': Task.CATEGORY_CHOICES,
        'priorities': Task.PRIORITY_CHOICES
    }
    return render(request, 'add_task.html', context)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('task_list')

@login_required
def mark_task_complete(request, task_id):
    from datetime import datetime
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.completed_at = datetime.now()
    task.save()
    messages.success(request, "Task marked as complete!")
    return redirect('task_list')

def csrf_test(request):
    """A simple view to test CSRF functionality."""
    if request.method == 'POST':
        test_value = request.POST.get('test_field', 'No value')
        return HttpResponse(f"CSRF test successful! Received: {test_value}")

    # Get the CSRF token for debugging
    csrf_token = get_token(request)
    csrf_cookie = request.COOKIES.get('csrftoken', 'No CSRF cookie')

    context = {
        'csrf_token': csrf_token,
        'csrf_cookie': csrf_cookie,
    }

    return render(request, 'csrf_test.html', context)

@csrf_exempt
def csrf_exempt_test(request):
    """A CSRF exempt view to test if the issue is with CSRF specifically."""
    if request.method == 'POST':
        test_value = request.POST.get('test_field', 'No value')
        return HttpResponse(f"CSRF exempt test successful! Received: {test_value}")

    return render(request, 'csrf_exempt_test.html')

def js_form_test(request):
    """A view to test form submission using JavaScript."""
    return render(request, 'js_form_test.html')
