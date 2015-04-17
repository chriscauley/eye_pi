from django import forms

from .models import Pair, DISPLAY_KEYS

class PairFilterForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(PairFilterForm,self).__init__(*args,**kwargs)
    for fname in ['r_sph','r_cyl','l_sph','l_cyl']:
      self.fields[fname].widget.attrs['step'] = 0.25
    for fname,field in self.fields.items():
      field.widget.attrs['max'] = 180
      field.widget.attrs['min'] = -180
      field.widget.attrs['class'] = "form-control"
      field.initial = 0
  def get_queryset(self):
    return Pair.objects.filter(selected=False,**self.cleaned_data)
  class Meta:
    model = Pair
    fields = DISPLAY_KEYS #+ ['number']
