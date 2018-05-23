from django.conf.urls import re_path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from user import views

urlpatterns = [
    # Views are defined in Djoser
    re_path(r'^users/me/$', djoser_views.UserView.as_view(), name='user-view'),
    re_path(r'^users/delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    re_path(r'^users/create/$', djoser_views.UserCreateView.as_view(), name='user-create'),

    # Views are defined in Rest Framework JWT
    re_path(r'^users/login/$', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    re_path(r'^users/login/refresh/$',
            jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
    re_path('^users/logout/$',
            views.UserLogoutAllView.as_view({'delete': 'destroy'}), name='user-logout-all'),
]
