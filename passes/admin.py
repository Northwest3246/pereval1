from django.contrib import admin
from .models import User, Coordinates, Level, Pass, Image

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'fam', 'name', 'phone']
    search_fields = ['email', 'fam', 'name']

@admin.register(Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'height']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['winter', 'summer', 'autumn', 'spring']

@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'add_time', 'user']
    list_filter = ['status']
    search_fields = ['title', 'user__email']
    actions = ['accept_passes', 'reject_passes']

    def accept_passes(self, request, queryset):
        queryset.update(status='accepted')
    accept_passes.short_description = "Принять выбранные перевалы"

    def reject_passes(self, request, queryset):
        queryset.update(status='rejected')
    reject_passes.short_description = "Отклонить выбранные перевалы"

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['pass_object', 'title']


