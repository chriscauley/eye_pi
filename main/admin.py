from django.contrib import admin

from .models import Pair

class PairAdmin(admin.ModelAdmin):
  list_display = ('number','__unicode__','selected',)
  list_editable = ('selected',)
  list_filter = ('selected',)

admin.site.register(Pair,PairAdmin)
