from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView, FormView, UpdateView, TemplateView

from prtx_faq.models import FAQ, FAQCategory
from prtx_faq.forms import FAQCategoryForm, FAQForm
from prtx_faq.prtx import PRTX


class FAQView(TemplateView):  # TODO
    template_name = 'prtx_faq/faq.{}.html'.format(PRTX)


class FAQList(ListView):
    model = FAQ
    context_object_name = 'questions'
    template_name = 'prtx_faq/faq_list.{}.html'.format(PRTX)


class FAQCreate(FormView):  # TODO
    template_name = 'prtx_faq/faq_create.{}.html'.format(PRTX)


class FAQEdit(UpdateView):  # TODO
    model = FAQ
    template_name = 'prtx_faq/faq_edit.{}.html'.format(PRTX)


class FAQDelete(DeleteView):  # TODO
    model = FAQ
    template_name = 'prtx_faq/faq_delete.{}.html'.format(PRTX)


def faq_up(request, *args, **kwargs):  # TODO
    pass


def faq_down(request, *args, **kwargs):  # TODO
    pass


class FAQCategoryList(ListView):
    model = FAQCategory
    context_object_name = 'categories'
    template_name = 'prtx_faq/faq_category_list.{}.html'.format(PRTX)


class FAQCategoryCreate(FormView):
    template_name = 'prtx_faq/faq_category_create.{}.html'.format(PRTX)
    form_class = FAQCategoryForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        kwargs = {'event': self.request.event.slug}
        if PRTX == 'pretix':
            kwargs['organizer'] = self.request.organizer.slug
        messages.success(self.request, _('Category created!'))
        return reverse('plugins:prtx_faq:faq.category.list', kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.request.event
        return kwargs


class FAQCategoryEdit(UpdateView):  # TODO
    model = FAQCategory
    template_name = 'prtx_faq/faq_category_edit.{}.html'.format(PRTX)


class FAQCategoryDelete(DeleteView):  # TODO
    model = FAQCategory
    template_name = 'prtx_faq/faq_category_delete.{}.html'.format(PRTX)


def faq_category_up(request, *args, **kwargs):  # TODO
    pass


def faq_category_down(request, *args, **kwargs):  # TODO
    pass
