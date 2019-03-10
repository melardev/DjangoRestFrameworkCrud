from rest_framework import serializers

from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'

    def get_description(self, instance):
        if self.context.get('include_details', False):
            return instance.description

    def to_representation(self, instance):
        response = super(TodoSerializer, self).to_representation(instance)
        if response.get('description') is None:
            response.pop('description')

        return response

    # Why do I need to override this? because if you use SerializerMethodField() that field will only be output
    # to the response, and never taken into account for write, to avoid this we override this
    def create(self, validated_data):
        return Todo.objects.create(description=self.context.get('description', ''), **validated_data)
