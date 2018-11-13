from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _
from prtx_faq.prtx import PRTX

if PRTX == 'pretalx':
    from pretalx.orga.signals import nav_event
elif PRTX == 'pretix':
    from pretix.control.signals import nav_event


@receiver(nav_event, dispatch_uid='faq_nav_entry')
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    kwargs = {'event': request.event.slug}
    if PRTX == 'pretix':
        kwargs['organizer'] = request.organizer.slug
    return [{
        'label': _('FAQ'),
        'icon': 'question-circle-o',
        'url': reverse('plugins:prtx_faq:faq.list', kwargs=kwargs),
        'active': 'faq' in url.url_name,
    }]
