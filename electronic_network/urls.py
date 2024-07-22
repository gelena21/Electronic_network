"""
Маршрутизация для приложения electronic_network.

Настраивает маршруты для API с использованием DRF Router:
- network-nodes: Маршрут для операций с узлами сети.
- products: Маршрут для операций с продуктами.
"""

from rest_framework.routers import SimpleRouter
from electronic_network.views import NetworkNodeViewSet, ProductViewSet

# Инициализация роутера
router = SimpleRouter()
router.register(r"network-nodes", NetworkNodeViewSet, basename="networknode")
router.register(r"products", ProductViewSet, basename="product")

# Определение маршрутов
urlpatterns = [
    # Включение маршрутов, определенных в роутере
]

urlpatterns += router.urls
