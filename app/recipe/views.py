from rest_framework import viewsets,authentication,permissions,mixins
from recipe.serializers import TagSerializer,IngredientSerializer
from core.models import Tag,Ingredient
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class RecipeAttrListViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Shorten your code by adding duplicate code"""
    authentication_classes =(authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class TagListView(RecipeAttrListViewSet):
    queryset = Tag.objects.all()

    serializer_class = TagSerializer


class IngredientListView(RecipeAttrListViewSet):

    queryset = Ingredient.objects.all()

    serializer_class = IngredientSerializer




#upadate tag model using APIView




# class updateTagView(APIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes =(permissions.IsAuthenticated,)
#     queryset = Tag.objects.all()
#
#     serializer_class = TagSerializer
#
#
#     def get_object(self, pk):
#         try:
#             return self.queryset.filter(pk=pk,user=self.request.user)
#         except Tag.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
