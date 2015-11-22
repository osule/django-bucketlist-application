from django.contrib import admin
from django.db.models import Count
from .models import Bucketlist, BucketlistItem


class BucketlistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',
                    'number_of_items',
                    'number_of_items_done',
                    'date_created',
                    'date_modified',)
    search_fields = ('name', 'user__first_name', 'user__last_name')
    date_hierarchy = 'date_created'
    exclude = ('date_created', 'date_updated',)

    def get_queryset(self, request):
        return super(BucketlistAdmin, self).get_queryset(
            request).annotate(num_items=Count('bucketlistitem'))

    def number_of_items(self, obj):
        return obj.num_items

    def number_of_items_done(self, obj):
        return obj.num_items_done()

admin.site.register(Bucketlist, BucketlistAdmin)  # registers Bucketlist model


class BucketlistItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',
                    'done', 'date_created',
                    'date_modified',)
    search_fields = ('name', 'user__first_name', 'user__last_name')
    date_hierarchy = 'date_created'
    exclude = ('date_created', 'date_updated',)

# registers BucketlistItem model
admin.site.register(BucketlistItem, BucketlistItemAdmin)
