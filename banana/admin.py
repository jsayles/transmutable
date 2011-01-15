from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import *

class CompletedItemAdmin(admin.ModelAdmin):
	list_display = ('user', 'modified')
admin.site.register(CompletedItem, CompletedItemAdmin)

class WorkDocAdmin(admin.ModelAdmin):
	list_display = ('user', 'modified')
admin.site.register(WorkDoc, WorkDocAdmin)