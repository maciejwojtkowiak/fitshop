from django.views.generic.detail import SingleObjectMixin
from django.db.models import F

class VisitCounter(SingleObjectMixin):
    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        old_visits = obj.visits
        obj.visits = F('visits') + 1
        obj.save()
        obj.visits = old_visits + 1
        return obj 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['visits'] = self.object.visits
        return context