from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'prtx_faq'
    verbose_name = 'A FAQ plugin for pretalx and pretix'

    class PretixPluginMeta:
        name = ugettext_lazy('Frequently Asked Questions')
        author = 'Tobias Kunze'
        description = ugettext_lazy('An FAQ plugin for pretalx and pretix')
        visible = True
        version = '1.0.0'

    class PretalxPluginMeta:
        name = ugettext_lazy('Frequently Asked Questions')
        author = 'Tobias Kunze'
        description = ugettext_lazy('An FAQ plugin for pretalx and pretix')
        visible = True
        version = '1.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'prtx_faq.PluginApp'
