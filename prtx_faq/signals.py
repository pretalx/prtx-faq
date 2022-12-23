from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

from prtx_faq.prtx import PRTX

if PRTX == "pretalx":
    from pretalx.orga.signals import nav_event

    @receiver(nav_event, dispatch_uid="faq_nav_entry")
    def navbar_info(sender, request, **kwargs):
        url = resolve(request.path_info)
        kwargs = {"event": request.event.slug}
        return [
            {
                "label": _("FAQ"),
                "icon": "question-circle-o",
                "url": reverse("plugins:prtx_faq:faq.list", kwargs=kwargs),
                "active": "faq" in url.url_name,
            }
        ]

elif PRTX == "pretix":
    from pretix.control.signals import nav_event

    @receiver(nav_event, dispatch_uid="faq_nav_entry")
    def navbar_info(sender, request, **kwargs):
        url = resolve(request.path_info)
        kwargs = {
            "event": request.event.slug,
            "organizer": request.organizer.slug,
        }
        return [
            {
                "label": _("FAQ"),
                "icon": "question-circle-o",
                "url": reverse("plugins:prtx_faq:faq.list", kwargs=kwargs),
                "active": False,
                "children": [
                    {
                        "label": _("Categories"),
                        "url": reverse(
                            "plugins:prtx_faq:faq.category.list", kwargs=kwargs
                        ),
                        "parent": reverse("plugins:prtx_faq:faq.list", kwargs=kwargs),
                        "active": "faq.category" in url.url_name,
                    },
                    {
                        "label": _("Questions"),
                        "url": reverse("plugins:prtx_faq:faq.list", kwargs=kwargs),
                        "parent": reverse("plugins:prtx_faq:faq.list", kwargs=kwargs),
                        "active": "faq" in url.url_name
                        and "category" not in url.url_name,
                    },
                ],
            },
        ]
