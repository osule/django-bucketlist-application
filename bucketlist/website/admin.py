from django.contrib import admin

from .models import Bucketlist, BucketlistItem

class BucketlistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',
                    'bucketlistitem_count_done',
                    'bucketlistitem_count', 'date_created', 
                    'date_modified',)
    search_fields = ('name', 'user__first_name', 'user__last_name')
    date_hierarchy = 'date_created'
    exclude = ('date_created', 'date_updated')

admin.site.register(Bucketlist, BucketlistAdmin) # registers Bucketlist model

class BucketlistItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',
                    'done', 'date_created',
                    'date_modified',)
    search_fields = ('name', 'user__first_name', 'user__last_name')
    date_hierarchy = 'date_created'
    exclude = ('date_created', 'date_updated',)

admin.site.register(BucketlistItem, BucketlistItemAdmin) # registers BucketlistItem model