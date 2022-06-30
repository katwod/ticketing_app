from django.contrib import admin
from .models import Ticket, Assistant
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class AssistantInLine(admin.StackedInline):
    model = Assistant
    can_delete = False
    verbose_name_plural = 'Assistants'

class CustomUser (UserAdmin):
    inlines = (AssistantInLine, )

admin.site.register(Ticket)

admin.site.unregister(User)
admin.site.register(User, CustomUser)

#admin.site.register(Assistant)
