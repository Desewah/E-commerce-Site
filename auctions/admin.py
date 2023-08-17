from django.contrib import admin
from .models import *

# Register your models here.
class CommentSectionAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'time_created', 'active')
    list_filter = ('active', 'time_created')
    search_fields = ('author', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(CommentSection)
admin.site.register(Bid)
