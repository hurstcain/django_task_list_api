from django.test import TestCase, Client
from django.urls import reverse
import json

from TasksAPI.models import Tasks
from TasksAPI.serializers import TaskSerializerCreate, TaskSerializerDetail


client = Client()


class GetAPIRootTest(TestCase):
    """
    Тестирование главной страницы
    """

    def test_get_api_root(self):
        response = client.get(reverse('api-root'))
        self.assertEqual(response.status_code, 200)


class GetAllTasksTest(TestCase):
    """
    Тестирование метода GET для всех задач
    """

    def setUp(self):
        Tasks.objects.create(header='Задача 1', text='Какой-то текст', completion_date='2022-02-20')
        Tasks.objects.create(header='Задача 2', text='Какой-то текст', completion_date='2022-02-22')
        Tasks.objects.create(header='Задача 3', text='Какой-то текст', completion_date='2022-02-13')

    def test_get_all_tasks(self):
        response = client.get(reverse('tasks-list'))
        content = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 3)


class CreateTaskTest(TestCase):
    """
    Тестирование метода POST
    """

    def setUp(self):
        self.valid_task = {
            'header': 'Task 1',
            'text': 'Some task',
            'completion_date': '2022-02-22'
        }
        self.invalid_task1 = {
            'header': 'Task 1',
            'text': 'Some task',
            'completion_date': '2022-112-92'
        }
        self.invalid_task2 = {
            'text': 'Some task',
            'completion_date': '2022-02-20'
        }

    def test_create_task(self):
        response = client.post(
            reverse('tasks-list'),
            data=self.valid_task,
            content_type='application/json'
        )
        content = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, {
            'header': 'Task 1',
            'text': 'Some task',
            'completion_date': '2022-02-22'
        })

        response = client.post(
            reverse('tasks-list'),
            data=self.invalid_task1,
            content_type='application/json'
        )
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerCreate(data=self.invalid_task1)
        serializer.is_valid()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, serializer.errors)

        response = client.post(
            reverse('tasks-list'),
            data=self.invalid_task2,
            content_type='application/json'
        )
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerCreate(data=self.invalid_task2)
        serializer.is_valid()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, serializer.errors)


class GetTaskByIdTest(TestCase):
    """
    Тестирование метода GET для каждой отдельной задачи
    """

    def setUp(self):
        self.task = Tasks.objects.create(header='Задача 1', text='Какой-то текст', completion_date='2022-02-20')

    def test_get_task(self):
        response = client.get(reverse('task-detail', kwargs={'pk': self.task.pk}))
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerDetail(Tasks.objects.get(pk=self.task.pk))
        self.assertEqual(content, serializer.data)
        self.assertEqual(response.status_code, 200)

        response = client.get(reverse('task-detail', kwargs={'pk': 10}))
        content = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(content, {"response": "The object does not exist"},)
        self.assertEqual(response.status_code, 404)


class UpdateTaskTest(TestCase):
    """
    Тестирование методов PUT и PATCH
    """

    def setUp(self):
        self.task1 = Tasks.objects.create(header='Задача 1', text='Какой-то текст', completion_date='2022-02-20')
        self.task2 = Tasks.objects.create(header='Задача 2', text='Какой-то текст', completion_date='2022-02-10')
        self.valid_update = {
            'header': 'Task 1',
            'text': 'Some task',
            'completion_date': '2022-02-20',
            'is_completed': True
        }
        self.invalid_update = {
            'header': '',
            'text': 'Some task',
            'completion_date': '2022-02-20',
            'is_completed': True
        }

    def test_update_task(self):
        response = client.put(reverse('task-detail', kwargs={'pk': self.task1.pk}),
                              data=json.dumps(self.valid_update))
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerDetail(Tasks.objects.get(pk=self.task1.pk))
        self.assertEqual(content, serializer.data)
        self.assertEqual(response.status_code, 200)

        response = client.put(reverse('task-detail', kwargs={'pk': self.task1.pk}),
                              data=json.dumps(self.valid_update))
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerDetail(Tasks.objects.get(pk=self.task1.pk))
        self.assertEqual(content, serializer.data)
        self.assertEqual(response.status_code, 200)

        response = client.put(reverse('task-detail', kwargs={'pk': self.task2.pk}),
                              data=json.dumps(self.invalid_update))
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerDetail(data=self.invalid_update)
        serializer.is_valid()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, serializer.errors)

        response = client.put(reverse('task-detail', kwargs={'pk': self.task2.pk}),
                              data=json.dumps(self.invalid_update))
        content = json.loads(response.content.decode('UTF-8'))
        serializer = TaskSerializerDetail(data=self.invalid_update)
        serializer.is_valid()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, serializer.errors)


class DeleteTaskTest(TestCase):
    """
    Тестирование метода DELETE
    """

    def setUp(self):
        self.task1 = Tasks.objects.create(header='Задача 1', text='Какой-то текст', completion_date='2022-02-20')
        self.task2 = Tasks.objects.create(header='Задача 2', text='Какой-то текст', completion_date='2022-02-23')

    def test_delete_task(self):
        response = client.get(reverse('tasks-list'))
        content = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        response = client.delete(reverse('task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 204)
        response = client.get(reverse('tasks-list'))
        content = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)


class InvalidPageTest(TestCase):
    """
    Проверка доступа к несуществующей странице
    """

    def test_invalid_page(self):
        response = client.get('tasksss')
        self.assertEqual(response.status_code, 404)
