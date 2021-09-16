#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .comments.models import Comment
from .comments.serializers import CommentSerializer
from .models import Issue


class IssueUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = "users.User"
        fields = "email"


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Issue
        fields = ("title", "type", "description", "reporter", "comments", "assignee", "comments")

    def create(self, validated_data):
        comments = validated_data.pop("comments")
        instance = super(IssueSerializer, self).create(validated_data)
        for comment in comments:
            instance.comments.add(Comment.objects.create(value=comment.get('value'),
                                                         owner=validated_data.get("reporter")))
        return instance

    def update(self, instance, validated_data):
        if "comments" in validated_data:
            comments = validated_data.pop("comments")
        else:
            comments = list()
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        for comment in comments:
            instance.comments.add(Comment.objects.create(value=comment.get('value'),
                                                         owner=self.instance.reporter))
        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()

        return instance

