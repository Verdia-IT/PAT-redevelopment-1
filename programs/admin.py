from django.contrib import admin
from .models import Program, ProgramOutput, ProgramOverride
# Register your models here.

admin.site.register(Program)
admin.site.register(ProgramOutput)
admin.site.register(ProgramOverride)
