from django.urls import path, include
from .views import RegisterView, UserProfileView, ExamRequestViewSet, ApplicationViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'requests', ExamRequestViewSet, basename='exam-requests')
router.register(r'applications', ApplicationViewSet, basename='applications')

urlpatterns = [
    # The router generates all the URL patterns automatically
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profiles/me/', UserProfileView.as_view(), name='profile-me'),
    path('', include(router.urls)),
]