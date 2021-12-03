from rest_framework import viewsets
from rest_framework import permissions
from todo.domain.models.list import ListModel
from todo.domain.models.task import TaskModel
from todo.serializers import TaskSerializer
from django.db.models import Prefetch


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        tasks = TaskModel.objects.prefetch_related(
            Prefetch('list', queryset=ListModel.objects.filter(
                user=user))
        ).filter(
            list__user__id=user.id
        )
        return tasks
