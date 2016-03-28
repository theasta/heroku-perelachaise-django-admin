from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin, GeoModelAdmin

from backend.models import Sepulture, Personality, Identity, Info, Country

class InfoInline(admin.TabularInline):
    model = Info
    extra = 0
    readonly_fields = ['wikipedia']
    def wikipedia(self, obj):
         return ('<a href="%s">Wiki</a>' % (obj.link))
    wikipedia.allow_tags = True

class IdentityInline(admin.TabularInline):
    model = Identity
    extra = 0
    
class PersonalityInline(admin.TabularInline):
    model = Personality
    fields = ['fullname']
    readonly_fields = ['fullname']
    extra = 0

class PersonalityAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'rank')
    search_fields = ('lastname', 'firstname')
    ordering = ('rank', 'lastname')
    list_filter = ['enabled', 'rank']
    def full_name(self, obj):
        return ("%s %s" % (obj.firstname, obj.lastname))
    full_name.short_description = 'Name'
    inlines = [
        IdentityInline,
        InfoInline,
    ]

class SepultureAdmin(OSMGeoAdmin):
    readonly_fields = ('id', 'modified', 'longitude', 'latitude')
    ordering = ('section', 'longitude', 'latitude')
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    inlines = [ PersonalityInline ]
    default_zoom = 18
    default_lon = 2.3940475
    default_lat = 47.211029
    modifiable = True

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')
    
    
admin.site.register(Sepulture, SepultureAdmin)
admin.site.register(Personality, PersonalityAdmin)
admin.site.register(Country, CountryAdmin)