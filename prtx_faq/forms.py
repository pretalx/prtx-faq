from django_scopes.forms import SafeModelChoiceField
from i18nfield.forms import I18nModelForm

from prtx_faq.models import FAQ, FAQCategory
from prtx_faq.prtx import PRTX


class FAQCategoryForm(I18nModelForm):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        kwargs["locales"] = (
            self.event.settings.get("locales")
            if PRTX == "pretix"
            else self.event.locales
        )
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.event = self.event
        if not self.instance.position:
            self.instance.position = getattr(
                self.event.faq_categories.last(), "position", 1
            )
        super().save(*args, **kwargs)

    class Meta:
        model = FAQCategory
        fields = ("name", "hidden")


class FAQForm(I18nModelForm):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        kwargs["locales"] = (
            self.event.settings.get("locales")
            if PRTX == "pretix"
            else self.event.locales
        )
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = self.event.faq_categories.all()

    def save(self, *args, **kwargs):
        if not self.instance.position:
            self.instance.position = getattr(
                FAQ.objects.filter(category__event=self.event).last(), "position", 1
            )
        super().save(*args, **kwargs)

    class Meta:
        model = FAQ
        fields = ("category", "question", "answer", "tags", "hidden")
        field_classes = {
            "category": SafeModelChoiceField,
        }
