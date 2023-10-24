from django.contrib import admin

from .models import Follow, User


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'following',
        'user',
    )
    list_display_links = (
        'user',
    )
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
    )
    list_display_links = (
        'username',
    )
    search_fields = (
        'username',
    )
    list_filter = (
        'username',
    )


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, UserAdmin)
