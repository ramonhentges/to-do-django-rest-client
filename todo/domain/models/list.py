from typing import Dict
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from cerberus import Validator


class ListModel(models.Model):
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="lists",
                             on_delete=models.CASCADE)

    class Meta:
        app_label = 'todo'


def listValidator(data: Dict):
    schema = {'description': {'minlength': 5, 'maxlength': 20}, 'user': {}}
    v = Validator(schema)
    if v.validate(data):
        return data
    print(v.errors)
    raise serializers.ValidationError(v.errors)
