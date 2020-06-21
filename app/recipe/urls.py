from django.urls import include,path
from .views import TagListView,IngredientListView
from rest_framework.routers import DefaultRouter
from core.models import Tag

router = DefaultRouter()
router.register('tags',TagListView)
router.register('ingredient',IngredientListView)


app_name='recipe'
# user_list = TagListView.as_view({'get': 'list'})
# urlpatterns = [
# path('taglist/',user_list,name='tag-list')
urlpatterns = [
 path('',include(router.urls)),
 path('ingredient',include(router.urls))
# path('update/<int:pk>/', updateTagView.as_view()),
]
