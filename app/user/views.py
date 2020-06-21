from rest_framework import generics,authentication,permissions,mixins
from user.serializers import UserSerializer,AuthTokenSerializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response



# Create your views here.

class CreateUserView(generics.CreateAPIView, mixins.ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        serializer_class = UserSerializer
        return self.list(request, *args, **kwargs)






class CreateTokenView(ObtainAuthToken):

        serializer_class = AuthTokenSerializers
        renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UpdateUser(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes =(permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
