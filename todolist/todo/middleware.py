import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class CSRFDebugMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        try:
            if request.method == 'POST':
                csrf_cookie = request.COOKIES.get('csrftoken', 'No CSRF cookie')
                csrf_header = request.META.get('HTTP_X_CSRFTOKEN', 'No CSRF header')
                csrf_form = request.POST.get('csrfmiddlewaretoken', 'No CSRF in form')

                logger.info(f"CSRF Debug - Cookie: {csrf_cookie}")
                logger.info(f"CSRF Debug - Header: {csrf_header}")
                logger.info(f"CSRF Debug - Form: {csrf_form}")

                # Log if tokens don't match
                if csrf_cookie != csrf_header and csrf_header != 'No CSRF header':
                    logger.warning(f"CSRF token mismatch - Cookie vs Header")
                if csrf_cookie != csrf_form and csrf_form != 'No CSRF in form':
                    logger.warning(f"CSRF token mismatch - Cookie vs Form")
        except Exception as e:
            logger.error(f"Error in CSRF Debug Middleware: {e}")

        response = self.get_response(request)
        return response


class DatabaseErrorMiddleware(MiddlewareMixin):
    """Middleware to handle database errors gracefully."""

    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def process_exception(self, request, exception):
        from django.db import OperationalError
        from django.shortcuts import render

        if isinstance(exception, OperationalError):
            if 'no such column: todo_task.priority' in str(exception):
                logger.error("Database error: Priority column doesn't exist. Run migrations.")
                context = {
                    'error_title': 'Database Schema Error',
                    'error_message': 'The database schema needs to be updated. Please run migrations.',
                    'error_details': str(exception),
                    'error_resolution': 'Run "python manage.py migrate" to update the database schema.'
                }
                return render(request, 'error.html', context, status=500)

        return None