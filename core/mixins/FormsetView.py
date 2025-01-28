from django.urls import resolve
from django.views.generic.edit import FormMixin


class FormsetView(FormMixin):
    """
    A mixin to manage a view with formsets
    """

    update_formset_after_save = False

    def get_named_formsets(self):
        return {}

    # Optionally implement this method
    def post_form_valid(self, form):
        pass

    def get_context_data(self, **kwargs):
        context = super(FormsetView, self).get_context_data(**kwargs)
        context['formsets'] = {}
        formsets = self.get_named_formsets()
        for name, formset_factory in formsets.items():
            formset_get_initial_func = getattr(self, 'formset_{0}_get_initial'.format(name), None)
            if formset_get_initial_func is not None:
                data = self.request.POST or None
                files = self.request.FILES or None
                context['formsets'][name] = formset_factory(data=data, files=files, initial=formset_get_initial_func(), prefix=name)
            else:
                context['formsets'][name] = formset_factory(prefix=name)
        return context

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        for formset_name, formset_class in named_formsets.items():
            formset_instance = formset_class(self.request.POST, self.request.FILES, prefix=formset_name)
            if not formset_instance.is_valid():
                errors = formset_instance.errors
                form.errors += errors
                return self.form_invalid(form)

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.

        for formset_name, formset_class in named_formsets.items():
            formset_instance = formset_class(self.request.POST, self.request.FILES, prefix=formset_name)
            if formset_instance.is_valid():
                formset_save_func = getattr(self, 'formset_{0}_valid'.format(formset_name), None)
                if formset_save_func is not None:
                    formset_save_func(formset_instance, self.object)
                else:
                    formset_instance.save()

        self.post_form_valid(form)

        return super(FormsetView, self).form_valid(form)