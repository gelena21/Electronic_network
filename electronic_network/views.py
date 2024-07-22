"""
Представления для приложения electronic_network.

Содержит:
- index: Функция для отображения стартовой страницы.
- NetworkNodeViewSet: Представление для управления узлами сети с поддержкой фильтрации.
- ProductViewSet: Представление для управления продуктами.
"""

from rest_framework import viewsets
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode, Product
from .permissions import IsActiveEmployee
from .serializers import NetworkNodeSerializer, ProductSerializer


def index(request):
    """
    Отображает стартовую страницу приложения.

    Параметры:
    - request: HTTP-запрос, содержащий информацию о запросе.

    Returns:
    - HttpResponse: Отображение шаблона 'index.html'.
    """
    return render(request, "index.html")


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Представление для управления узлами сети (NetworkNode).

    Обеспечивает стандартные операции CRUD (создание, чтение, обновление, удаление) и поддержку фильтрации.

    Атрибуты:
    - queryset: Запрос для получения всех объектов NetworkNode.
    - serializer_class: Сериализатор, используемый для преобразования данных модели в формат JSON и обратно.
    - filter_backends: Бэкенды для фильтрации запросов.
    - filterset_fields: Поля, по которым можно фильтровать объекты.
    - permission_classes: Классы разрешений, определяющие доступ к представлению.

    Методы:
    - list: Возвращает список объектов NetworkNode.
    - create: Создает новый объект NetworkNode.
    - retrieve: Возвращает один объект NetworkNode по его идентификатору.
    - update: Обновляет существующий объект NetworkNode.
    - partial_update: Частично обновляет существующий объект NetworkNode.
    - destroy: Удаляет объект NetworkNode.
    """

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["contact", "contact__country"]
    permission_classes = [IsActiveEmployee]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Представление для управления продуктами (Product).

    Обеспечивает стандартные операции CRUD (создание, чтение, обновление, удаление).

    Атрибуты:
    - queryset: Запрос для получения всех объектов Product.
    - serializer_class: Сериализатор, используемый для преобразования данных модели в формат JSON и обратно.
    - permission_classes: Классы разрешений, определяющие доступ к представлению.

    Методы:
    - list: Возвращает список объектов Product.
    - create: Создает новый объект Product.
    - retrieve: Возвращает один объект Product по его идентификатору.
    - update: Обновляет существующий объект Product.
    - partial_update: Частично обновляет существующий объект Product.
    - destroy: Удаляет объект Product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
