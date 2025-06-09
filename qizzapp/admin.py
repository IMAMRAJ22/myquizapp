from django.contrib import admin
from .models import Userlogin,Statusbar,Quizz,Option,Admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Show 4 option fields

class QuizAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


admin.site.register(Userlogin)
admin.site.register(Statusbar)
admin.site.register(Quizz, QuizAdmin)
admin.site.register(Admin)


# Register your models here.
