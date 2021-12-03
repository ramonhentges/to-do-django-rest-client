from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from todo.permissions import AddToGroupAccessPolicy
from todo.serializers import AddUserToGroupSerializer, CreateUpdateUserSerializer, RetrieveUserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = RetrieveUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        actions = [
            'create'
        ]
        if self.action in actions:
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user)

    def get_serializer_class(self):
        actions = [
            'create',
            'update',
            'partial_update'
        ]
        if self.action in actions:
            return CreateUpdateUserSerializer
        return self.serializer_class


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated, AddToGroupAccessPolicy])
def add_user_to_group(request, userId):
    try:
        user = User.objects.get(pk=userId)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AddUserToGroupSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
