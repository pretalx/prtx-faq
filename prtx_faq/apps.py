from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class PluginApp(AppConfig):
    name = "prtx_faq"
    verbose_name = "A FAQ plugin for pretalx and pretix"

    class PretixPluginMeta:
        name = gettext_lazy("Frequently Asked Questions")
        author = "Tobias Kunze"
        description = gettext_lazy("An FAQ plugin for pretalx and pretix")
        visible = True
        version = "1.0.0"

    class PretalxPluginMeta:
        name = gettext_lazy("Frequently Asked Questions")
        author = "Tobias Kunze"
        description = gettext_lazy("An FAQ plugin for pretalx and pretix")
        visible = True
        version = "1.0.1"

    def ready(self):
        from . import signals  # NOQA
