from django.db import models

class RegistryNumber(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер')
    type = models.CharField(max_length=10, verbose_name='Тип')
    time = models.DateTimeField(auto_now=True, verbose_name='Последнее обращение')
    exists = models.BooleanField(default=True, verbose_name='Субьект малого или среднего предпринимательства')

    def __str__(self):
        return self.type
