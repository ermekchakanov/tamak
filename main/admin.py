from django.contrib import admin
from .models import UserProfile, Feedback, Comment 

admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(Comment)