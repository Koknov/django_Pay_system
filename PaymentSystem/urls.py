from django.urls import path, re_path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import TransactionsViewSet, TransactionsView, UsersViewSet, UsersView, RegistrationAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Paysystem API",
        default_version='v1',
        description="Welcome",
        terms_of_service="https://www.other.org",
        contact=openapi.Contact(email="example@mail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "PaySystem"

router = DefaultRouter()
router.register(r'usersViewSet', UsersViewSet)

router.register(r'transactionViewSet', TransactionsViewSet)

urlpatterns = router.urls + [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('users/', UsersView.as_view()),
    path('transactions/', TransactionsView.as_view()),
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', views.TokenObtainPairView.as_view()),
    path('login/refresh/', views.TokenRefreshView.as_view()),
]
