from django.db import models


class Tasks(models.Model):
    """
    Модель задач
    id - уникальный идентификатор задачи
    header - заголовок
    text - текст задачи (сделала текст задачи необязательным полем)
    completion_date - дата выполнения задачи
    is_completed - отметка о факте выполнения задачи (true/false, по умолчанию false)
    При выгрузке данных из БД данные будут сортироваться по полям is_completed и completion_date
    """

    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=300)
    text = models.TextField(blank=True, null=True)
    completion_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_completed', 'completion_date']
