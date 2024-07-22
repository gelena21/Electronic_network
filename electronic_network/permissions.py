"""
Определения разрешений для приложения electronic_network.

Содержит:
- IsActiveEmployee: Проверяет, что пользователь активен и аутентифицирован.
"""

from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """
    Разрешение для проверки, что пользователь активен и аутентифицирован.

    Проверяет, что пользователь:
    - аутентифицирован (request.user.is_authenticated)
    - активен (request.user.is_active)
    """

    def has_permission(self, request, view):
        """
        Проверяет разрешение для запроса.

        Параметры:
        - request: Объект запроса.
        - view: Представление, к которому применяется разрешение.

        Returns:
            bool: Разрешено ли выполнение запроса.
        """
        return request.user and request.user.is_authenticated and request.user.is_active
