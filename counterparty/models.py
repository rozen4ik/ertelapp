from django.db import models


class CounterpartyWarrantyObligations(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=150)
    contract = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Контрагент: {self.name} - Тип: {self.type}"

    class Meta:
        verbose_name = "контрагент: гарантийные обязательства"
        verbose_name_plural = "контрагенты: гарантийные обязательства"


class CounterpartyTO(models.Model):
    name = models.CharField(max_length=250, )
    type = models.CharField(max_length=150)
    contract = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Контрагент: {self.name} - Тип: {self.type}"

    class Meta:
        verbose_name = "контрагент: техническое обслуживание"
        verbose_name_plural = "контрагенты: техническое обслуживание"
