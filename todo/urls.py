from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from todo.views.users import UserViewSet, add_user_to_group
from todo.views.lists import ListViewSet
from todo.views.groups import GroupViewSet
from todo.views.tasks import TaskViewSet
from rest_framework.authtoken import views as tokenview
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'lists', ListViewSet)
router.register(r'tasks', TaskViewSet)

api_urls = format_suffix_patterns(
    [path('usergroup/<int:userId>', add_user_to_group)])
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', tokenview.obtain_auth_token),
    path('admin/', admin.site.urls)
] + api_urls
