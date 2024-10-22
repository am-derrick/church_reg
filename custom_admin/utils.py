from django.contrib.auth.decorators import user_passes_test

def super_admin_required(view_func):
    """decorator for super_admin access"""
    decorated_view_func = user_passes_test(lambda u: u.is_authenticated and u.is_super_admin(),
                                           login_url='login')(view_func)
    return decorated_view_func

def admin_required(view_func):
    """decorator for super_admin and min_admin access"""
    decorated_view_func = user_passes_test(lambda u: u.is_authenticated and
                                           (u.is_super_admin() or u.is_mini_admin()),
                                           login_url='login')(view_func)
    return decorated_view_func


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