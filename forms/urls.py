from django.urls import path, include
from rest_framework.routers import DefaultRouter
from forms.views import FormViewSet, SubmitResponseView

router = DefaultRouter()
router.register(r"", FormViewSet, basename="form")

urlpatterns = [
    path("", include(router.urls)),
    path('submissions/', SubmitResponseView.as_view(), name='submit-response')
]