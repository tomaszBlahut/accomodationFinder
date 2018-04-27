from django.views.generic import TemplateView


class HomeView(TemplateView):
    number_list = [x for x in range(5)]
    template_name = "./home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_list'] = self.number_list
        return context
