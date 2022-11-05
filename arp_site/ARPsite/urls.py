from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # /admin: admin panel
    path('admin/', admin.site.urls),
    # /: client panel
    path('', include('home.urls')),

]
