from django.db import models


class Counterparty(models.Model):
    name = models.CharField(max_length=250)
    work_name = models.CharField(max_length=250)
    type = models.CharField(max_length=150)
    contract = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Контрагент: {self.name} - Тип: {self.type}"

    class Meta:
        verbose_name = "контрагента"
        verbose_name_plural = "контрагент"
