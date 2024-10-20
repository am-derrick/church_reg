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