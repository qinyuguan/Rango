from django.http import JsonResponse
from django.shortcuts import redirect


def user_required(ajax=False):
    def decoration(func):
        def warpper(request, *args, **kwargs):
            if not request.user.is_authenticated and ajax==False:
                return redirect('rango:login')
            if not request.user.is_authenticated and ajax==True:
                return JsonResponse({'code': 500, 'status': 'failed',
                                     'msg': 'Please Login.'})
            if request.user.is_authenticated and request.user.is_superuser and ajax == False:
                return redirect('rango:index')
            if request.user.is_authenticated and request.user.is_superuser and ajax == True:
                return JsonResponse({'code': 500, 'status': 'failed',
                                     'msg': 'You have no permission. Please log in the common user account.'})
            return func(request, *args, **kwargs)

        return warpper

    return decoration


def admin_required(ajax=False):
    def decoration(func):
        def warpper(request, *args, **kwargs):
            if not request.user.is_authenticated and ajax==False:
                return redirect('rango:login')
            if not request.user.is_authenticated and ajax==True:
                return JsonResponse({'code': 500, 'status': 'failed',
                                     'msg': 'Please Login.'})
            if request.user.is_authenticated and request.user.is_superuser == False and ajax == False:
                return redirect('rango:index')
            if request.user.is_authenticated and request.user.is_superuser == False and ajax == True:
                return JsonResponse({'code': 500, 'status': 'failed',
                                     'msg': 'You have no permission. Please log in the common user account.'})

            return func(request, *args, **kwargs)

        return warpper

    return decoration
