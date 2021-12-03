from typing import Dict
from todo.domain.models.list import ListModel
from django.db import models
from rest_framework import serializers
from todo.validator import Validator


class TaskModel(models.Model):
    description = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    list = models.ForeignKey(
        ListModel, related_name="tasks", on_delete=models.CASCADE)

    class Meta:
        app_label = 'todo'


def taskValidator(data: Dict):
    print(data)
    schema = {'description': {'minlength': 3, 'maxlength': 100},
              'done': {'type': 'boolean'}, 'list': {'type': 'list'}}
    v = Validator(schema)
    if v.validate(data):
        return data
    raise serializers.ValidationError(v.errors)
