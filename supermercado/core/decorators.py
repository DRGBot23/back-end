from django.shortcuts import redirect

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("funcionario_id"):
            return redirect("login")
        return func(request, *args, **kwargs)
    return wrapper

def role_required(*tipos_permitidos):
    def decorator(func):
        def wrapper(request, *args, **kwargs):

            tipo = request.session.get("funcionario_tipo")
            user_id = request.session.get("funcionario_id")

            if not user_id:
                return redirect("login")

            if tipo not in tipos_permitidos:
                return redirect("dashboard")

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


