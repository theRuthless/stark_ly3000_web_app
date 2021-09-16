from rest_framework import routers
from .views import WorkLogViewSet

router = routers.SimpleRouter()

router.register('', WorkLogViewSet)
urlpatterns = router.urls
