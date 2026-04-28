from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from uploader.router import router as uploader_router
from core.views import (
    CategoriaViewSet, 
    EditoraViewSet, 
    LivroViewSet, 
    UserViewSet, 
    AutorViewSet, 
    UserRegistrationView
)

# Configuração do Router
router = DefaultRouter()
router.register(r'livros', LivroViewSet, basename='livro')
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'editoras', EditoraViewSet, basename='editora')
router.register(r'usuarios', UserViewSet, basename='usuario')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/media/', include(uploader_router.urls)),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('api/registro/', UserRegistrationView.as_view(), name='user_registration'),
    
    path('api/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
