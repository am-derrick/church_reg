from django.contrib import messages
from django.shortcuts import redirect

def permission_required(permission_func):
    """decorator to check for permission of user or else display that they don't have access"""
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if permission_func(request.user):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('admin_dashboard')
        return wrapped_view
    return decorator

def is_super_admin(user):
    """function for super_admin access"""
    return user.is_authenticated and user.is_super_admin()

def is_admin(user):
    """function for super_admin and min_admin access"""
    return user.is_authenticated and (user.is_super_admin() or user.is_mini_admin())


def get_page_range(paginator, page, max_pages=9):
    """Helper function to generate a number of pages
    for pagination with a range or elipsis
    """
    current_page = page.number
    total_pages = paginator.num_pages

    # If total pages is less than max_pages, show all pages
    if total_pages <= max_pages:
        return range(1, total_pages + 1)
    
    # Calculates the ranges of pages to show
    start_page = max(current_page - 4, 1)
    end_page = min(current_page + 4, total_pages)

    # Adjust rnage if near beginning or end
    if current_page <= 4:
        end_page = max_pages
    elif current_page >= total_pages - 4:
        start_page = total_pages - max_pages + 1

    page_range = []

    # Add first page and elipsis
    if start_page > 1:
        page_range.append(1)
        if start_page > 2:
            page_range.append('...')

    # Add main range of pages
    page_range.extend(range(start_page, end_page +1))

    # Add last page and elipsis
    if end_page < total_pages:
        if end_page < total_pages - 1:
            page_range.append('...')
        page_range.append(total_pages)

    return page_range

def get_client_ip(request):
    """Get client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWADED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip