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


class FAQCategoryList(ListView):  # TODO
    model = FAQCategory
    template_name = 'prtx_faq/faq_category_list.{}.html'.format(PRTX)


class FAQCategoryCreate(FormView):  # TODO
    template_name = 'prtx_faq/faq_category_create.{}.html'.format(PRTX)


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
