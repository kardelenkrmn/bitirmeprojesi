from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass

admin.site.register(Profil)

admin.site.register(Adress)


admin.site.register(Comment)



