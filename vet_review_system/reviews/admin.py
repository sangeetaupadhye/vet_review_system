from django.contrib import admin
from .models import Veterinarian

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'rating')
    readonly_fields = ('rating',)
