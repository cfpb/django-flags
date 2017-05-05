from django.db import models


class FlagState(models.Model):
    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=64, default='boolean')
    value = models.CharField(max_length=127, default='True')

    class Meta:
        app_label = 'flags'
        unique_together = ('name', 'condition', 'value')

    def __str__(self):
        return "{name} is enabled when {condition} is {value}".format(
            name=self.name, condition=self.condition, value=self.value)
