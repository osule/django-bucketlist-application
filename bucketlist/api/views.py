from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import BucketlistSerializer, UserSerializer, \
BucketlistWithItemsSerializer, BucketlistItemSerializer, \
BucketlistItemCreateSerializer
from website.models import Bucketlist, BucketlistItem


class UserViewSet(viewsets.ModelViewSet):
    """defines the user view behavior"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BucketlistList(generics.ListCreateAPIView):
    """defines the bucketlist list view behaviour"""
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,)
    paginate_by = 100

    def get_queryset(self):
        """specifies the queryset used for the serialization"""
        q = self.request.GET.get('q', None)
        if q:
            return Bucketlist.search(q)
        return Bucketlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """saves the serialize POST data creating a new bucketlist"""
        serializer.save(user_id=self.request.user.id)


class BucketlistDetail(generics.RetrieveUpdateDestroyAPIView):
    """defines the bucketlist detail view behaviour.
    Comes with Read, Update and Delete.
    """
    queryset = Bucketlist
    serializer_class = BucketlistWithItemsSerializer
    permission_classes = (IsAuthenticated,)

    def get_query(self):
        """specifies the object used for `update`,
         `retrieve`, `destroy` actions"""
        return get_object_or_404(Bucketlist, pk=self.kwargs.get('pk'))


class BucketlistItemCreate(generics.ListCreateAPIView):
    """defines the bucketlist create view behaviour.
    """
    model = BucketlistItem
    serializer_class = BucketlistItemSerializer

    def get_queryset(self):
        """specifies the queryset used the serialization"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(Bucketlist, pk=pk)
        return BucketlistItem.objects.filter(
            user=self.request.user, bucketlist=bucketlist)

    def perform_create(self, serializer):
        """saves the serialize POST data creating a new bucketlist"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(
            Bucketlist, pk=pk, user_id=self.request.user.id)
        serializer.save(bucketlist=bucketlist, user_id=self.request.user.id)

class BucketlistItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """defines the bucketlist detail view behaviour.
    Comes with Read, Update, and Delete.
    """
    queryset = BucketlistItem
    serializer_class = BucketlistItemSerializer
    
    def get_object(self):
        """specifies the object used for `update`,
         `retrieve`, `destroy` actions"""
        pk_item = self.kwargs.get('pk_item')
        return get_object_or_404(BucketlistItem, pk=pk_item)

