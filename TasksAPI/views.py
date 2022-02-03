from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse

from TasksAPI.models import Tasks
from TasksAPI.serializers import TaskSerializerList, TaskSerializerCreate, TaskSerializerDetail


@api_view(['GET'])
def api_root(request):
    """
    Стартовая страница
    """

    return JsonResponse({
        'Get tasks': reverse('tasks-list', request=request)
    })


@api_view(['GET', 'POST'])
def tasks_list(request):
    """
    Представление для вывода списка задач, а также для добавления задачи.
    Если используется метод GET (вывод списка), то используется сериализатор TaskSerializerList,
    а если метод POST (добавление новой задачи), то сериализатор TaskSerializerCreate.
    """

    if request.method == 'GET':
        tasks = Tasks.objects.all()
        serializer = TaskSerializerList(tasks, context={'request': request},  many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializerCreate(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tasks_detail(request, pk):
    """
    Представление для отображения конкретной задачи, а также для ее редактирования и удаления
    (методы GET, PUT, PATCH, DELETE).
    """

    try:
        task = Tasks.objects.get(pk=pk)
    except Tasks.DoesNotExist:
        return JsonResponse({"response": "The object does not exist"}, status=404)

    if request.method == 'GET':
        serializer = TaskSerializerDetail(task)
        return JsonResponse(serializer.data, status=200)

    elif request.method == 'PUT' or request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = TaskSerializerDetail(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({"response": "The object has been deleted"}, status=204)


# Представления на основе классов
#
# from rest_framework import generics
#
#
# class TasksList(generics.ListCreateAPIView):
#     """
#     Представление для вывода списка задач, а также для добавления задачи.
#     Если используется метод GET (вывод списка), то используется сериализатор TaskSerializerList,
#     а если метод POST (добавление новой задачи), то - сериализатор TaskSerializerCreate.
#     """
#
#     queryset = Tasks.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return TaskSerializerList
#         elif self.request.method == 'POST':
#             return TaskSerializerCreate
#
#
# class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Представление для отображения конкретной задачи, а также для ее редактирования и удаления
#     (методы GET, PUT, PATCH, DELETE).
#     """
#
#     queryset = Tasks.objects.all()
#     serializer_class = TaskSerializerDetail
