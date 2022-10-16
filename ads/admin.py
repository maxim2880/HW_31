from django.contrib import admin

from ads.models import Categories, Ads

from users.models import Location, User

admin.site.register(Categories)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Ads)