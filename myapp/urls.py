from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('player_info', views.PlayerViewSet,basename='player_dataset')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('register/<str:login>/<str:password>/', views.ItemAPIView.as_view(), name='item_api'),
    path('update-achieves/<str:login>/<str:achieve_type>/<int:type_value>/', views.UpdateAchievesView.as_view(), name='update-achieves'),
]