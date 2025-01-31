from django.contrib import admin
from .models import VideoModel, GenreModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class VideoInline(admin.TabularInline):
    model = VideoModel.genres.through  # Many-to-many Beziehung
    extra = 1  # Gibt an, wie viele leere Felder standardmäßig angezeigt werden
    
# VideoModel im Admin registrieren
@admin.register(VideoModel)
class VideoAdmin(ImportExportModelAdmin):
    list_display = ['title', 'created_at', 'description']
    filter_horizontal = ('genres',)  

# GenreModel im Admin registrieren
@admin.register(GenreModel)
class GenreAdmin(ImportExportModelAdmin):
    list_display = ['name']
    inlines = [VideoInline] 

class VideoResource(resources.ModelResource):
    class Meta:
        model = VideoModel

class GenreResource(resources.ModelResource):
    class Meta:
        model = GenreModel