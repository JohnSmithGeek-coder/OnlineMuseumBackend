from django.urls import path

from .views import CommentsView, DynamicView, DynamicsView, ObjectView, ObjectsView, StarView, StarsView, UserInfoView
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/<username>/', UserInfoView.as_view(), name='UserInfo'),
    path('objects/', ObjectsView.as_view(), name='objects'),
    path('object/<id>/', ObjectView.as_view(), name='object'),
    path('dynamics/', DynamicsView.as_view(), name='dynamics'),
    path('dynamic/<id>/', DynamicView.as_view(), name='dynamic'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('stars/', StarsView.as_view(), name='stars'),
    path('star/<id>/', StarView.as_view(), name='star'),
]
