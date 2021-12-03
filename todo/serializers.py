from django.contrib.auth.models import User, Group
from rest_framework import serializers
from todo.domain.models.task import TaskModel, taskValidator
from todo.domain.models.list import ListModel, listValidator
from todo.permissions import GroupAccessPolicy
from todo.validator import Validator


class GroupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        schema = {'name': {'minlength': 5, 'maxlength': 20}}
        v = Validator(schema)
        if v.validate(data):
            return data
        raise serializers.ValidationError(v.errors)

    class Meta:
        model = Group
        fields = ['id', 'name']
        access_policy = GroupAccessPolicy


class RetrieveUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class CreateUpdateUserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        schema = {'username': {'minlength': 5, 'maxlength': 20},
                  'email': {'is email': 'not_required'}, 'password': {}}
        v = Validator(schema)
        if v.validate(data):
            return data
        raise serializers.ValidationError(v.errors)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, obj):
        ret = super(CreateUpdateUserSerializer, self).to_representation(obj)
        ret.pop('password')
        return ret

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AddUserToGroupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        schema = {'groups': {}}
        v = Validator(schema)
        if v.validate(data):
            return data
        raise serializers.ValidationError(v.errors)

    class Meta:
        model = User
        fields = ['groups']


class TaskSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if self.context['view'].request.user != data['list'].user:
            raise serializers.ValidationError(
                {'list': ['invalid list']})
        return taskValidator(data)

    class Meta:
        model = TaskModel
        fields = ['id', 'description', 'done', 'list']


class RetrieveListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = ListModel
        fields = ['id', 'description', 'tasks']


class ListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    def validate(self, data):
        return listValidator(data)

    class Meta:
        model = ListModel
        fields = ['id', 'description', 'user']
