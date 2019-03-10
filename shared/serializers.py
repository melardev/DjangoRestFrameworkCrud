import math

from rest_framework import serializers


class AppBaseSerializer(serializers.Serializer):
    success = serializers.SerializerMethodField(method_name='is_success')
    full_messages = serializers.SerializerMethodField()

    def get_full_messages(self, data):
        return []

    def get_full_messages(self, data):
        if type(data) == list:
            return data
        elif type(data) == str:
            return [data]

    def is_success(self, data):
        return self.context.get('success', False)

class SuccessSerializer(AppBaseSerializer):

    def is_success(self, data):
        return True


class ErrorSerializer(serializers.Serializer):

    def is_success(self, data):
        return False
