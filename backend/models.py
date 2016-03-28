from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models
 
class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    country = models.CharField(max_length=24)
    def __unicode__(self):
            return self.country
    class Meta:
        managed = False
        db_table = 'country'
        verbose_name_plural = "Countries"
        
class Sepulture(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    geog = models.GeometryField(geography=True) 
    # geog = models.TextField(blank=True, null=True)  # This field type is a guess.
    section = models.SmallIntegerField()
    urn = models.CharField(max_length=8)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        lat = self.latitude
        if not lat:
            lat = '-'
        else:
            lat = str(lat)
        
        lon = self.longitude
        if not lon:
            lon = '-'
        return ("Section: %d (%s , %s)" % (self.section, lon, lat))
        
    class Meta:
        managed = True
        db_table = 'sepulture'

class Personality(models.Model):
    id = models.AutoField(primary_key=True)
    inscription = models.CharField(max_length=64, blank=True)
    fullname = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64, blank=True)
    lastname = models.CharField(max_length=64)
    birth = models.IntegerField()
    death = models.IntegerField()
    rank = models.SmallIntegerField()
    sepulture = models.ForeignKey(
        'Sepulture',
        on_delete=models.CASCADE
    )
    cenotaph = models.BooleanField()
    nationalities = models.ManyToManyField(Country, db_table='personality_country')
    picture = models.CharField(max_length=128, blank=True)
    enabled = models.BooleanField()
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.fullname;  
    class Meta:
        managed = False
        db_table = 'personality'
        verbose_name = "Personality"
        verbose_name_plural = "Personalities"
        
class Identity(models.Model):
    id = models.AutoField(primary_key=True)
    personality = models.ForeignKey('Personality', on_delete=models.CASCADE)
    LANG = (
        ('fr', 'French'),
        ('en', 'English'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('es', 'Spanish'),
        ('ja', 'Japanese'),
    )
    lang = models.CharField(max_length=2,
                            choices=LANG,
                            default='fr')     
    fullname = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64, blank=True)
    lastname = models.CharField(max_length=64)
    def original_fullname(self):
        return self.personality.fullname
    def __unicode__(self):
        return ("%s (%s)" % (self.original_fullname(), self.lang))
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'identity'
        unique_together = ("lang", "personality")
        verbose_name = "Localized Identitity"
        verbose_name_plural = "Localized Identities"


class Info(models.Model):
    id = models.AutoField(primary_key=True)
    personality = models.ForeignKey('Personality', on_delete=models.CASCADE)                         
    LANG = (
        ('fr', 'French'),
        ('en', 'English'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('es', 'Spanish'),
        ('ja', 'Japanese'),
    )
    lang = models.CharField(max_length=2,
                            choices=LANG,
                            default='fr')
    link = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=64, blank=True)
    modified = models.DateTimeField(auto_now=True)
    def original_fullname(self):
        return self.personality.fullname
    def __unicode__(self):
        return ("%s (%s)" % (self.original_fullname(), self.lang))

    class Meta:
        managed = False
        db_table = 'info'
        unique_together = ("lang", "personality")
        verbose_name = "Localized Info"
        verbose_name_plural = "Localized Infos"


class PersonalityCountry(models.Model):
    personality = models.ForeignKey(Personality, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'personality_country'
        unique_together = (('personality', 'country'),)


# class SpatialRefSys(models.Model):
#     srid = models.IntegerField(primary_key=True)
#     auth_name = models.CharField(max_length=256, blank=True, null=True)
#     auth_srid = models.IntegerField(blank=True, null=True)
#     srtext = models.CharField(max_length=2048, blank=True, null=True)
#     proj4text = models.CharField(max_length=2048, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'spatial_ref_sys'
