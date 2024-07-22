"""
Модели для приложения electronic_network.

Содержит определения моделей:
- Contact: Контактная информация для узлов сети.
- NetworkNode: Узел сети с иерархией и задолженностью.
- Product: Продукты, связанные с узлами сети.
"""

from django.db import models
from django.core.exceptions import ValidationError


class Contact(models.Model):
    """
    Модель для хранения контактной информации узлов сети.

    Поля:
    - email: Адрес электронной почты.
    - country: Страна, в которой расположен контакт.
    - city: Город, в котором расположен контакт.
    - street: Улица, на которой расположен контакт.
    - building_number: Номер здания.

    Методы:
    - __str__: Возвращает строковое представление контакта.
    """

    email = models.EmailField(
        verbose_name="email",
    )
    country = models.CharField(max_length=60, verbose_name="страна")
    city = models.CharField(
        max_length=60,
        verbose_name="город",
    )
    street = models.CharField(max_length=60, verbose_name="улица")
    building_number = models.CharField(max_length=30, verbose_name="номер дома")

    def __str__(self):
        """
        Возвращает строковое представление контакта, включающее все его поля.
        """
        return (
            f"{self.email} - {self.country} - {self.city} - {self.street}"
            f" - {self.building_number}"
        )

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"


class NetworkNode(models.Model):
    """
    Модель для узла сети.

    Поля:
    - name: Название узла сети.
    - contact: Связанный контактный объект (один к одному).
    - supplier: Связанный узел-снабженец (многие к одному).
    - level: Уровень иерархии узла.
    - debt: Задолженность узла перед поставщиком.
    - created_at: Дата и время создания узла.

    Методы:
    - get_hierarchy_level: Возвращает уровень иерархии узла.
    - clean: Проверяет, что уровень иерархии не превышает 3 звена.
    - __str__: Возвращает строковое представление узла.
    """

    LEVEL_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255, verbose_name="название узла")
    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
        related_name="network_node",
        verbose_name="контакты узла",
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="связанный узел",
    )
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="уровень иерархии")
    debt = models.DecimalField(
        max_digits=16, decimal_places=2, verbose_name="задолженность", default=0
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="время создания")

    def get_hierarchy_level(self):
        """
        Возвращает уровень иерархии узла, начиная с корневого узла.

        Рекурсивно проверяет уровень узла по отношению к его поставщику.

        Returns:
            int: Уровень иерархии узла.
        """

        def get_level(node, level=0):
            if node.supplier:
                return get_level(node.supplier, level + 1)
            return level

        return get_level(self)

    def clean(self):
        """
        Проверяет, что уровень иерархии узла не превышает 3 звена.

        Если уровень иерархии больше 2, вызывает ValidationError.
        """
        super().clean()
        if self.get_hierarchy_level() > 2:
            raise ValidationError("Максимальная иерархия не должна превышать 3 звена.")

    def __str__(self):
        """
        Возвращает строковое представление узла, включающее его название.
        """
        return f"{self.name}"

    class Meta:
        verbose_name = "узел сети"
        verbose_name_plural = "узлы сети"


class Product(models.Model):
    """
    Модель для продукта, связанного с узлом сети.

    Поля:
    - name: Название продукта.
    - model: Модель продукта.
    - market_date: Дата выхода продукта на рынок.
    - network_node: Узел сети, к которому относится продукт.

    Методы:
    - __str__: Возвращает строковое представление продукта.
    """

    name = models.CharField(max_length=256, verbose_name="название продукта")
    model = models.CharField(max_length=256, verbose_name="модель продукта")
    market_date = models.DateField(
        verbose_name="дата выхода на рынок",
    )
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="узел сети",
    )

    def __str__(self):
        """
        Возвращает строковое представление продукта, включающее название, модель и
        дату выхода на рынок.
        """
        return f"{self.name} - {self.model} - {self.market_date}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
