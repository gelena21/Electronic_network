"""
Конфигурация административной панели для приложения electronic_network.

Этот модуль настраивает административные интерфейсы для моделей Contact, NetworkNode и Product.

Настроенные классы:
- ContactAdmin: Административный интерфейс для модели Contact
- NetworkNodeAdmin: Административный интерфейс для модели NetworkNode
- ProductAdmin: Административный интерфейс для модели Product

Функции:
- ContactAdmin: Отображает поля email, country, city, street и building_number; поддерживает поиск по email, country и city.
- NetworkNodeAdmin: Отображает поля name, contact, supplier, level, debt, created_at; поддерживает фильтрацию по city и country, поиск по name и city. Поддерживает действие по очистке задолженности.
- ProductAdmin: Отображает поля name, model, market_date, network_node; поддерживает поиск по name и model.
"""

from django.contrib import admin
from electronic_network.models import Contact, NetworkNode, Product


class ContactAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Contact.

    Отображает следующие поля:
    - email
    - country
    - city
    - street
    - building_number

    Поддерживает поиск по:
    - email
    - country
    - city
    """

    list_display = ("email", "country", "city", "street", "building_number")
    search_fields = ("email", "country", "city")


class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели NetworkNode.

    Отображает следующие поля:
    - name
    - contact
    - supplier
    - level
    - debt
    - created_at

    Поддерживает фильтрацию по:
    - contact__city
    - contact__country

    Поддерживает поиск по:
    - name
    - contact__city

    Поддерживает действие по очистке задолженности:
    - Очистка задолженности перед поставщиком
    """

    list_display = ("name", "contact", "supplier", "level", "debt", "created_at")
    list_filter = ("contact__city", "contact__country")
    search_fields = ("name", "contact__city")

    actions = ["clear_debt"]

    def clear_debt(self, request, queryset):
        """
        Очистить задолженность перед поставщиком для выбранных объектов.

        Параметры:
        - request: Объект запроса Django.
        - queryset: Критерии для выбора объектов для действия.
        """
        queryset.update(debt=0)

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


class ProductAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Product.

    Отображает следующие поля:
    - name
    - model
    - market_date
    - network_node

    Поддерживает поиск по:
    - name
    - model
    """

    list_display = ("name", "model", "market_date", "network_node")
    search_fields = ("name", "model")


admin.site.register(Contact, ContactAdmin)
admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Product, ProductAdmin)
