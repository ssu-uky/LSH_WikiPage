from django.db import models
from common.models import CommonModel


class Board(CommonModel):
    title = models.TextField(
        max_length=50,
        null=False,
        blank=False,
    )

    content = models.TextField(
        max_length=200,
        null=False,
        blank=False,
    )

    related_board = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.title