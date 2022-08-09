from django.db import models


class CounterpartyWarrantyObligations(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=150)
    contract = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Контрагент: {self.name} - Тип: {self.type}"

    class Meta:
        verbose_name = "гарантийные обязательства"
        verbose_name_plural = "гарантийные обязательства"


class CounterpartyTO(models.Model):
    name = models.CharField(max_length=250, )
    type = models.CharField(max_length=150)
    contract = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Контрагент: {self.name} - Тип: {self.type}"

    class Meta:
        verbose_name = "техническое обслуживание"
        verbose_name_plural = "техническое обслуживание"
