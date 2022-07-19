from rest_framework import routers
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = router.urls