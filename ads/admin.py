from django.contrib import admin

from ads.models import Categories, Location, User, Ads

admin.site.register(Categories)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Ads)