from django.db import models
from django.utils.translation import gettext_lazy as _
from django_scopes import ScopedManager
from i18nfield.fields import I18nCharField, I18nTextField

from prtx_faq.prtx import PRTX


class FAQCategory(models.Model):
    event = models.ForeignKey(
        to="pretixbase.Event" if PRTX == "pretix" else "event.Event",
        on_delete=models.CASCADE,
        related_name="faq_categories",
    )
    name = I18nCharField(verbose_name=_("Name"), max_length=180)
    position = models.PositiveIntegerField(verbose_name=_("Position"))
    hidden = models.BooleanField(default=False)

    objects = ScopedManager(
        **(
            dict(organizer="event__organizer")
            if PRTX == "pretix"
            else dict(event="event")
        )
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("position", "id")


class FAQ(models.Model):
    category = models.ForeignKey(
        to=FAQCategory,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Category"),
    )
    question = I18nCharField(verbose_name=_("Question"))
    answer = I18nTextField(verbose_name=_("Answer"))
    tags = models.CharField(
        null=True,
        blank=True,
        max_length=180,
        verbose_name=_("Tags"),
        help_text=(
            "Tags can help people find related questions. Please enter the tags separated by commas."
        ),
    )
    position = models.PositiveIntegerField(verbose_name=_("Position"))
    hidden = models.BooleanField(default=False)

    objects = ScopedManager(
        **(
            dict(organizer="category__event__organizer")
            if PRTX == "pretix"
            else dict(event="category__event")
        )
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ("category__position", "position", "id")
