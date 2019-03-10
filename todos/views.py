# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from shared.serializers import AppBaseSerializer
from todos.models import Todo
from todos.serializers import TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_queryset(self):
        if self.request.path.endswith('pending'):
            self.queryset = self.queryset.filter(completed=False)
        elif 'completed' in self.request.path:
            self.queryset = self.queryset.filter(completed=True)

        self.queryset = self.queryset.order_by('-created_at')
        return self.queryset

    def list(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(self.get_queryset(), many=True).data
        return Response(serialized_data)

    def create(self, request, **kwargs):
        serializer_data = request.data
        serializer_context = {
            'include_details': True,
            'description': request.data['description']
        }
        serializer = TodoSerializer(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        Todo.objects.all().delete()
        return Response('', status=status.HTTP_204_NO_CONTENT)


class TodoDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_object(self):
        try:
            return Todo.objects.get(pk=self.kwargs[self.lookup_field])
        except Todo.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo is None:
            return Response(AppBaseSerializer('Todo not Found').data)
        todo.title = request.data['title']

        description = request.data.get('description', None)

        if description is not None:
            todo.description = description

        todo.completed = request.data.get('completed', False)
        todo.save()
        data = self.serializer_class(todo, context={'include_details': True}).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        try:
            todo = Todo.objects.get(pk=kwargs['pk'])
            data = self.serializer_class(todo, context={'include_details': True}).data
            return Response(data)
        except Todo.DoesNotExist:
            return Response(AppBaseSerializer('Todo not Found').data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo is not None:
            todo.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(AppBaseSerializer('Todo not found').data,
                            status=status.HTTP_404_NOT_FOUND)
