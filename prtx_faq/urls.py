from django.urls import re_path

from prtx_faq.prtx import PRTX

from . import views


def get_urls():
    urls = []
    data = (
        (r"faq/$", views.FAQList.as_view(), "faq.list"),
        (r"faq/new/$", views.FAQCreate.as_view(), "faq.create"),
        (r"faq/(?P<pk>[0-9]+)/$", views.FAQEdit.as_view(), "faq.edit"),
        (r"faq/(?P<pk>[0-9]+)/delete/$", views.FAQDelete.as_view(), "faq.delete"),
        (r"faq/(?P<pk>[0-9]+)/up/$", views.faq_up, "faq.up"),
        (r"faq/(?P<pk>[0-9]+)/down/$", views.faq_down, "faq.down"),
        (r"faq/category/$", views.FAQCategoryList.as_view(), "faq.category.list"),
        (
            r"faq/category/new/$",
            views.FAQCategoryCreate.as_view(),
            "faq.category.create",
        ),
        (
            r"faq/category/(?P<pk>[0-9]+)/$",
            views.FAQCategoryEdit.as_view(),
            "faq.category.edit",
        ),
        (
            r"faq/category/(?P<pk>[0-9]+)/delete/$",
            views.FAQCategoryDelete.as_view(),
            "faq.category.delete",
        ),
        (r"faq/category/(?P<pk>[0-9]+)/up/$", views.faq_category_up, "faq.category.up"),
        (
            r"faq/category/(?P<pk>[0-9]+)/down/$",
            views.faq_category_down,
            "faq.category.down",
        ),
    )
    if PRTX == "pretix":
        base = r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/"
        for entry in data:
            urls.append(re_path(base + entry[0], entry[1], name=entry[2]))

    elif PRTX == "pretalx":
        base = r"^orga/event/(?P<event>[^/]+)/"
        for entry in data:
            urls.append(re_path(base + entry[0], entry[1], name=entry[2]))
        urls.append(
            re_path(r"^(?P<event>[^/]+)/faq/$", views.FAQView.as_view(), name="faq"),
        )
    return urls


urlpatterns = get_urls()

if PRTX == "pretix":
    from pretix.multidomain import event_url

    event_patterns = [
        event_url(r"^faq/$", views.FAQView.as_view(), name="faq"),
    ]
