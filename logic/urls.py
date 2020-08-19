from rest_framework import routers
from logic.views import UsersViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet)


urlpatterns = router.urls
