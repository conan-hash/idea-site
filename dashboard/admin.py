from django.contrib import admin
from .models import Idea

# Register your models here.
@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'identifier')