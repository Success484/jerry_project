from django.contrib import admin
from .models import Profile, Transfer, Chatbox, UserProfile, IMFVerification

# Register the custom user model
admin.site.register(Profile)
admin.site.register(Transfer)
admin.site.register(Chatbox)
admin.site.register(UserProfile)
admin.site.register(IMFVerification)