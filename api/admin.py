from django.contrib import admin

# Register your models here.
from api.models import User, FarmerProfile, Farm, Case\
    #, CaseImg

admin.site.register(User)
admin.site.register(FarmerProfile)
admin.site.register(Farm)
admin.site.register(Case)
#admin.site.register(CaseImg)