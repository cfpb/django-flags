from django.db import models


class FlagState(models.Model):
    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=64, default="boolean")
    value = models.CharField(max_length=127, default="True")
    required = models.BooleanField(default=False)

    class Meta:
        app_label = "flags"
        unique_together = ("name", "condition", "value")

    def __str__(self):
        required_str = " (required)" if self.required else ""
        return (
            f"{self.name} is enabled when {self.condition} is "
            f"{self.value}{required_str}"
        )


class FlagMetadata(models.Model):
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64)
    value = models.TextField()

    class Meta:
        app_label = "flags"
        unique_together = ("name", "key")

    def __str__(self):
        return f"{self.name} ({self.key}: {self.value})"
