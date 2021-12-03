from rest_framework import viewsets
from rest_framework import permissions
from todo.domain.models.list import ListModel
from todo.serializers import ListSerializer, RetrieveListSerializer


class ListViewSet(viewsets.ModelViewSet):
    queryset = ListModel.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context["request"]
        serializer.save(user=request.user)

    def get_queryset(self):
        user = self.request.user
        return ListModel.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveListSerializer
        return self.serializer_class
