from django.contrib import admin

from .models import Pair

class PairAdmin(admin.ModelAdmin):
  list_display = ('number','selected','__unicode__',)
  list_editable = ('selected',)
  list_filter = ('selected',)
  search_fields = ('number',)

admin.site.register(Pair,PairAdmin)
