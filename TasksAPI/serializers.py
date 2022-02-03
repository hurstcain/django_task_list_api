from rest_framework import serializers

from TasksAPI.models import Tasks


class TaskSerializerList(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения списка задач.
    Выводит дополнительное поле link с ссылкой на конкретную задачу.
    """

    link = serializers.HyperlinkedIdentityField(view_name='task-detail')

    class Meta:
        model = Tasks
        fields = ('link', 'id', 'header', 'text', 'completion_date', 'is_completed')


class TaskSerializerCreate(serializers.ModelSerializer):
    """
    Сериализатор, используемый для создания задачи.
    При этом используются только поля header, text и completion_date.
    """

    class Meta:
        model = Tasks
        fields = ('header', 'text', 'completion_date')


class TaskSerializerDetail(serializers.ModelSerializer):
    """
    Сериализатор, используемый для отображения конкретной задачи, а также для редактирования задачи.
    Для редактирования доступны поля header, text, completion_date и is_completed.
    """

    class Meta:
        model = Tasks
        fields = ('header', 'text', 'completion_date', 'is_completed')
