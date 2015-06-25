from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Pair
from .forms import PairFilterForm, ImportForm
from utils import from_xlx

def home(request):
  form = PairFilterForm(request.GET or None)
  queryset = []
  if form.is_valid():
    queryset = form.get_queryset()
    if "rando" in request.GET:
      queryset = Pair.objects.order_by("?")
    queryset = list(queryset)[:50]
    for pair in queryset:
      pair.cache_differences(request.REQUEST)
    queryset = sorted(queryset,key=lambda p: p.cached_distance)
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

@staff_member_required
def import_xls(request):
  form = ImportForm(request.POST or None,request.FILES or None)
  if form.is_valid():
    xls = request.FILES['xls']
    fname = '/tmp/%s'%xls.name
    f = open(fname,'w')
    f.write(xls.read())
    f.close()
    total,dups = from_xlx(fname)
    messages.success(request,"%s pairs added to the database"%total)
    if dups:
      messages.success(request,"%s pairs duplicates detected (number was already in database)"%dups)
    return HttpResponseRedirect(request.path)
  values = {'form': form}
  return TemplateResponse(request,"import_xls.html",values)
