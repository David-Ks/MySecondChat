from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', index.as_view(), name='index'),
    path('chat/<str:room_name>/', room, name='room'),
    path('reg/', Registration.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('createroom/', CreateRoom.as_view(), name='createroom'),
]
