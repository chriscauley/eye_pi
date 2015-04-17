from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Pair
from .forms import PairFilterForm

def home(request):
  form = PairFilterForm(request.GET or None)
  queryset = []
  if form.is_valid():
    queryset = list(form.get_queryset())
    for pair in queryset:
      pair.cache_differences(request.REQUEST)
  values = {
    'form': form,
    'queryset': queryset,
  }
  return TemplateResponse(request,"index.html",values)

redirect = lambda request,url: HttpResponseRedirect(url)

@csrf_exempt
def select(request,pk):
  pair = Pair.objects.get(pk=pk)
  pair.selected = True
  pair.save()
  return HttpResponse('')

@csrf_exempt
def unselect(request,pk):
  pair = Pair.objects.get(pk=pk)
  pair.selected = False
  pair.save()
  return HttpResponse('')
