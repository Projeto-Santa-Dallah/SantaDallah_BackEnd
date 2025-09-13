from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from uploader.router import router as uploader_router

from core.views import UserViewSet, CategoriaViewSet, ProdutoViewSet, TamanhoViewSet, OrcamentoViewSet, PrecoQtdViewSet, EnderecoViewSet, AvaliacaoViewSet, PedidoViewSet

router = DefaultRouter()
router.register(r"avaliacoes", AvaliacaoViewSet) 
router.register(r"categorias", CategoriaViewSet) 
router.register(r"enderecos", EnderecoViewSet) 
router.register(r"orcamentos", OrcamentoViewSet) 
router.register(r"pedidos", PedidoViewSet, basename="pedido") 
router.register(r"precos-quantidades", PrecoQtdViewSet) 
router.register(r"produtos", ProdutoViewSet) 
router.register(r"tamanhos", TamanhoViewSet) 
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path("api/media/", include(uploader_router.urls)),
    # API
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
