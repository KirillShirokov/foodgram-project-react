from django.contrib import admin

from .models import Follow


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

admin.site.register(Follow, FollowAdmin)
