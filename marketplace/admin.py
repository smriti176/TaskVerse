from django.contrib import admin
from .models import FreelancerProfile, Project, Bid

admin.site.register(FreelancerProfile)
admin.site.register(Project)
admin.site.register(Bid)