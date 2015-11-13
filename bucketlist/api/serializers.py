from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import serializers
from website.models import Bucketlist, BucketlistItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Defines the user API representation.
    """
    class Meta:
        model = User
        fields = ('username', 'email')
    

class BucketlistSerializer(serializers.ModelSerializer):
    """Defines the bucketlist API representation.
    """
    created_by = serializers.SerializerMethodField('get_creator')
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by')
    
    def get_creator(self, obj):
        return obj.user.id
 

class BucketlistWithItemsSerializer(BucketlistSerializer):
    """Defines the bucketlist API representation with children items.
    """
    items = serializers.SerializerMethodField('get_bucketlistitems')
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    
 
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'items', 
                  'date_created', 'date_modified', 'created_by')
    
    def get_bucketlistitems(self, obj):
        queryset = list(BucketlistItem.objects.filter(bucketlist=obj))
        return [
            BucketlistItemSerializer(bucketlistitem).data \
            for bucketlistitem in queryset]


class BucketlistItemSerializer(serializers.ModelSerializer):
    """Defines the bucketlistitem API representation.
    """
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    
    class Meta:
        model = BucketlistItem
        fields = ('id', 'name', 'done', 'date_created', 'date_modified')
        
class BucketlistItemCreateSerializer(serializers.ModelSerializer):
    """Defines the bucketlistitem API representation for creation of a new
    bucketlistitem.
    """
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%I:%S")
    
    class Meta:
        model = BucketlistItem