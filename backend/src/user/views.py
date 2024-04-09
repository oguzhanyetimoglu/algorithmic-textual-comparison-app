from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin
from .models import User
from .serializers import UserSerializer, UserCreateSerializer


class CreateListUser(generics.GenericAPIView, mixins.CreateModelMixin,
                     mixins.ListModelMixin):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateDeleteUser(generics.GenericAPIView, mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user is not None:
            return self.request.user
        raise Http404
