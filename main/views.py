from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .models import Pair
from .forms import PairFilterForm

def home(request):
  form = PairFilterForm(request.GET or None)
  queryset = []
  if form.is_valid():
    queryset = form.get_queryset()
  values = {
    'form': form,
    'queryset': queryset,
  }
  return TemplateResponse(request,"index.html",values)

redirect = lambda request,url: HttpResponseRedirect(url)
