from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DeleteView, FormView, ListView, TemplateView, UpdateView,
)

from prtx_faq.forms import FAQCategoryForm, FAQForm
from prtx_faq.models import FAQ, FAQCategory
from prtx_faq.prtx import PRTX

if PRTX == "pretix":
    from pretix.control.permissions import (
        EventPermissionRequiredMixin, event_permission_required,
    )

    class PermMixin(EventPermissionRequiredMixin):
        permission = "can_change_event_settings"

    perm_annotation = event_permission_required("can_change_event_settings")
else:
    from pretalx.common.mixins.views import PermissionRequired

    class PermMixin(PermissionRequired):
        permission_required = "orga.change_settings"

        def get_permission_object(self):
            return self.request.event

    def perm(func):
        return func

    perm_annotation = perm


class FAQView(TemplateView):
    template_name = f"prtx_faq/faq.{PRTX}.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["categories"] = (
            self.request.event.faq_categories.filter(hidden=False)
            .filter(questions__hidden=False)
            .distinct()
        )
        ctx["event"] = self.request.event
        ctx["organizer"] = getattr(self.request, "organizer", None)
        return ctx


class FAQList(PermMixin, ListView):
    model = FAQ
    context_object_name = "questions"
    template_name = f"prtx_faq/faq_list.{PRTX}.html"

    def get_queryset(self):
        return FAQ.objects.filter(category__event=self.request.event).order_by(
            "category__position", "position", "pk"
        )


class FAQCreate(PermMixin, FormView):
    template_name = f"prtx_faq/faq_create.{PRTX}.html"
    form_class = FAQForm

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Question created!"))
        return reverse("plugins:prtx_faq:faq.list", kwargs=kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs


class FAQEdit(PermMixin, UpdateView):
    model = FAQ
    template_name = f"prtx_faq/faq_edit.{PRTX}.html"
    form_class = FAQForm

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Question saved!"))
        return reverse("plugins:prtx_faq:faq.list", kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs


class FAQDelete(PermMixin, DeleteView):
    model = FAQ
    template_name = f"prtx_faq/faq_delete.{PRTX}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = FAQ.objects.get(
            category__event=self.request.event, pk=self.kwargs["pk"]
        )
        return context

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Question deleted!"))
        return reverse("plugins:prtx_faq:faq.list", kwargs=kwargs)


def faq_move(request, pk, up=True):
    try:
        question = FAQ.objects.get(category__event=request.event, pk=pk)
    except FAQ.DoesNotExist:
        raise Http404(_("The selected question does not exist."))
    questions = list(
        FAQ.objects.filter(category=question.category).order_by("position")
    )

    index = questions.index(question)
    if index != 0 and up:
        questions[index - 1], questions[index] = questions[index], questions[index - 1]
    elif index != len(questions) - 1 and not up:
        questions[index + 1], questions[index] = questions[index], questions[index + 1]

    for i, qst in enumerate(questions):
        if qst.position != i:
            qst.position = i
            qst.save()
    messages.success(request, _("The order of questions has been updated."))
    kwargs = {"event": request.event.slug}
    if PRTX == "pretix":
        kwargs["organizer"] = request.organizer.slug
    return reverse("plugins:prtx_faq:faq.list", kwargs=kwargs)


@perm_annotation
def faq_up(request, **kwargs):
    return redirect(faq_move(request, kwargs.get("pk"), up=True))


@perm_annotation
def faq_down(request, **kwargs):
    return redirect(faq_move(request, kwargs.get("pk"), up=False))


class FAQCategoryList(PermMixin, ListView):
    model = FAQCategory
    context_object_name = "categories"
    template_name = f"prtx_faq/faq_category_list.{PRTX}.html"

    def get_queryset(self):
        return self.request.event.faq_categories.all().order_by("position", "pk")


class FAQCategoryCreate(PermMixin, FormView):
    template_name = f"prtx_faq/faq_category_create.{PRTX}.html"
    form_class = FAQCategoryForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Category created!"))
        return reverse("plugins:prtx_faq:faq.category.list", kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs


class FAQCategoryEdit(PermMixin, UpdateView):
    model = FAQCategory
    template_name = f"prtx_faq/faq_category_edit.{PRTX}.html"
    form_class = FAQCategoryForm

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Category saved!"))
        return reverse("plugins:prtx_faq:faq.category.list", kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs


class FAQCategoryDelete(PermMixin, DeleteView):
    model = FAQCategory
    template_name = f"prtx_faq/faq_category_delete.{PRTX}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.request.event.faq_categories.get(
            pk=self.kwargs["pk"]
        )
        return context

    def get_success_url(self):
        kwargs = {"event": self.request.event.slug}
        if PRTX == "pretix":
            kwargs["organizer"] = self.request.organizer.slug
        messages.success(self.request, _("Category deleted!"))
        return reverse("plugins:prtx_faq:faq.category.list", kwargs=kwargs)


def faq_category_move(request, pk, up=True):
    try:
        category = request.event.faq_categories.get(pk=pk)
    except FAQCategory.DoesNotExist:
        raise Http404(_("The selected category does not exist."))
    categories = list(request.event.faq_categories.order_by("position"))

    index = categories.index(category)
    if index != 0 and up:
        categories[index - 1], categories[index] = (
            categories[index],
            categories[index - 1],
        )
    elif index != len(categories) - 1 and not up:
        categories[index + 1], categories[index] = (
            categories[index],
            categories[index + 1],
        )

    for i, cat in enumerate(categories):
        if cat.position != i:
            cat.position = i
            cat.save()
    messages.success(request, _("The order of categories has been updated."))
    kwargs = {"event": request.event.slug}
    if PRTX == "pretix":
        kwargs["organizer"] = request.organizer.slug
    return reverse("plugins:prtx_faq:faq.category.list", kwargs=kwargs)


@perm_annotation
def faq_category_up(request, **kwargs):
    return redirect(faq_category_move(request, kwargs.get("pk"), up=True))


@perm_annotation
def faq_category_down(request, **kwargs):
    return redirect(faq_category_move(request, kwargs.get("pk"), up=False))
