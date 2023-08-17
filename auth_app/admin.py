from django.contrib import admin

from auth_app import models as auth_models


@admin.register(auth_models.ViaPraetoriaUserProfile)
class ViaPraetoriaProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(auth_models.ViaPraetoriaUser)
class ViaPraetoriaUserAdmin(admin.ModelAdmin):
    pass
