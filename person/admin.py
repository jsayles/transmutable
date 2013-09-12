from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from models import *

 
class StyledAdmin(admin.ModelAdmin):
	save_on_top=True

class PhotoAdmin(StyledAdmin):
	list_display = ('image', 'thumb')
admin.site.register(Photo, PhotoAdmin)

class InviteRequestAdmin(StyledAdmin):
	list_display = ('email', 'created')

admin.site.register(InviteRequest, InviteRequestAdmin)

class UserProfileInline(admin.StackedInline):
	raw_id_fields = ('user', 'photo', 'invites')
	model = UserProfile
	max_num = 1

class UserAndProfileAdmin(UserAdmin):
	inlines = [UserProfileInline] 
admin.site.unregister(User)
admin.site.register(User, UserAndProfileAdmin)

class InviteAdmin(StyledAdmin):
	list_display = ('id', 'invite_owner', 'sent_to', 'used_by', 'created')

	def invite_owner(self, invite):
		if not invite.inviter.all(): return None
		return invite.inviter.all()[0]

admin.site.register(Invite, InviteAdmin)
