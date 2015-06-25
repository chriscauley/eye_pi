from django import forms

from .models import Pair, DISPLAY_KEYS

def validate_25(value):
  if float(value)%0.25 > 0.01:
    raise forms.ValidationError("Please enter a number that's a multiple of 0.25")

def validate_neg(value):
  if float(value) > 0:
    raise forms.ValidationError("Please enter a number less than or equal to 0.")

def validate_number(value):
  try:
    float(value)
  except TypeError:
    raise forms.ValidationError("Please enter a number.")

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
      if "cyl" in fname:
        field.widget.attrs['max'] = 0
  def get_queryset(self):
    return Pair.objects.filter(selected=False,**self.cleaned_data)

  def clean_r_cyl(self,*args,**kwargs):
    value = self.cleaned_data.get("r_cyl",None)
    validate_number(value)
    validate_25(value)
    validate_neg(value)
    return float(value)
  def clean_l_cyl(self,*args,**kwargs):
    value = self.cleaned_data.get("l_cyl",None)
    validate_number(value)
    validate_25(value)
    validate_neg(value)
    return float(value)

  def clean_r_sph(self,*args,**kwargs):
    value = self.cleaned_data.get("r_sph",None)
    validate_number(value)
    validate_25(value)
    return float(value)
  def clean_l_sph(self,*args,**kwargs):
    value = self.cleaned_data.get("l_sph",None)
    validate_number(value)
    validate_25(value)
    return float(value)

  def clean_r_axis(self,*args,**kwargs):
    value = self.cleaned_data.get("r_axis",None)
    validate_number(value)
    return float(value)
  def clean_l_axis(self,*args,**kwargs):
    value = self.cleaned_data.get("l_axis",None)
    validate_number(value)
    return float(value)

  class Meta:
    model = Pair
    fields = DISPLAY_KEYS #+ ['number']

class ImportForm(forms.Form):
  xls = forms.FileField()
