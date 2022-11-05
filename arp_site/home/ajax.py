from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from . import decorators


@decorators.logged
def login_page(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return JsonResponse({"result": True})
        else:
            return JsonResponse({"result": False, "error": "WD"}) # WD-Wrong Data
    if request.method == "GET":
        return JsonResponse({"result": request.user.is_authenticated})