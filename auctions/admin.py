from django.contrib import admin
from .models import Bid, Comments, User, Listing
# Register your models here.

admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Listing)
