from django.db import models


class FlagState(models.Model):
    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=64, default="boolean")
    value = models.CharField(max_length=127, default="True")
    required = models.BooleanField(default=False)

    class Meta:
        app_label = "flags"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "condition", "value"],
                name="flags_flagstate_unique_name_condition_value",
            )
        ]

    def __str__(self):
        return (
            "{name} is enabled when {condition} is {value}{required}".format(
                name=self.name,
                condition=self.condition,
                value=self.value,
                required=" (required)" if self.required else "",
            )
        )
