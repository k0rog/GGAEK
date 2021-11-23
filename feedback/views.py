from .forms import FeedbackForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class FeedbackView(CreateView):
    template_name = 'feedback.html'
    success_url = reverse_lazy('main')
    form_class = FeedbackForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.evaluation = form.cleaned_data['evaluation']
        self.object.save()

        return super().form_valid(form)
