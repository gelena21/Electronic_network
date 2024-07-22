"""
Сериализаторы для приложения electronic_network.

Содержит:
- ProductSerializer: Сериализация модели Product.
- ContactSerializer: Сериализация модели Contact.
- NetworkNodeSerializer: Сериализация модели NetworkNode с дополнительной обработкой.
"""

from rest_framework import serializers
from electronic_network.models import Product, Contact, NetworkNode


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Поля:
    - name: Название продукта.
    - model: Модель продукта.
    - market_date: Дата выхода продукта на рынок.
    - network_node: Узел сети, к которому относится продукт.
    """

    class Meta:
        model = Product
        fields = ("name", "model", "market_date", "network_node")


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Contact.

    Поля:
    - email: Адрес электронной почты.
    - country: Страна, в которой расположен контакт.
    - city: Город, в котором расположен контакт.
    - street: Улица, на которой расположен контакт.
    - building_number: Номер здания.

    Использует все поля модели.
    """

    class Meta:
        model = Contact
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.

    Поля:
    - name: Название узла сети.
    - contact: Сериализованный объект Contact, связанный с узлом.
    - hierarchy_level: Уровень иерархии узла (вычисляемый метод).
    - supplier: Связанный узел-снабженец.
    - level: Уровень иерархии узла.
    - debt: Задолженность узла перед поставщиком.
    - created_at: Дата и время создания узла.

    Методы:
    - get_hierarchy_level: Возвращает уровень иерархии узла и проверяет его.
    - create: Создает новый объект NetworkNode и связанный Contact.
    - update: Обновляет существующий объект NetworkNode и связанный Contact.
    """

    hierarchy_level = serializers.SerializerMethodField()
    contact = ContactSerializer()

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt",)

    def get_hierarchy_level(self, obj):
        """
        Возвращает уровень иерархии узла.

        Если уровень иерархии превышает 2, выбрасывает ошибку валидации.

        Параметры:
        - obj: Объект NetworkNode.

        Returns:
            int: Уровень иерархии узла.

        Raises:
            serializers.ValidationError: Если уровень иерархии превышает 2.
        """
        if obj.get_hierarchy_level() > 2:
            raise serializers.ValidationError(
                "Иерархия узлов не может превышать 3 уровня"
            )
        return obj.get_hierarchy_level()

    def create(self, validated_data):
        """
        Создает новый объект NetworkNode и связанный объект Contact.

        Параметры:
        - validated_data: Валидированные данные для создания NetworkNode.

        Returns:
            NetworkNode: Созданный объект NetworkNode.
        """
        contact_data = validated_data.pop("contact")
        contact = Contact.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact=contact, **validated_data)
        return network_node

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект NetworkNode и связанный объект Contact.

        Параметры:
        - instance: Объект NetworkNode для обновления.
        - validated_data: Валидированные данные для обновления NetworkNode.

        Returns:
            NetworkNode: Обновленный объект NetworkNode.
        """
        contact_data = validated_data.pop("contact")
        contact = instance.contact

        instance.name = validated_data.get("name", instance.name)
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.level = validated_data.get("level", instance.level)

        for attr, value in contact_data.items():
            setattr(contact, attr, value)
        contact.save()

        instance.save()
        return instance
