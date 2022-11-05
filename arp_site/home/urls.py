from django.urls import path
from . import views

urlpatterns = [
    # ./ main page
    path('home/', views.home_page),

    # ./login/                         login page : TO   AJAX try to log
    #                                             : FROM AJAX try to log
    path('login/', views.login_page),

    # ./guild/
    path('guild/', views.filler),

    # ./guild/<guild_id>/
    path('guild/<int:guild_id>/', views.filler),

    # ./guild/<guild_id>/member/
    path('guild/<int:guild_id>/member/', views.filler),

    # ./guild/<guild_id>/member/<member_id>/
    path('guild/<int:guild_id>/member/<int:member_id>', views.filler),

    # ./guild/<guild_id>/character
    path('guild/<int:guild_id>/character/', views.filler),

    # ./guild/<guild_id>/character/<character_id>/
    path('guild/<int:guild_id>/character/<int:character_id>', views.filler),
]
