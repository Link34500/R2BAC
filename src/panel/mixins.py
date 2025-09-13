from django.http import Http404

class PanelPageMixin:
  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_authenticated and self.request.user.is_staff:
      return super().dispatch(request, *args, **kwargs)
    raise Http404("Vous n'êtes pas autorisé à voir cette page")