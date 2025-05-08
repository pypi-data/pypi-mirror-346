"""AST visitor and plugin implementation for enforcing @allure.id() usage."""

import ast
from typing import Any, Generator, List, Tuple, Type


class AllureIdVisitor(ast.NodeVisitor):
    """AST-посетитель для поиска классов Scenario без декоратора @allure.id()."""

    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str, Type[Any]]] = []
        self.has_allure_import = False
        self.decorators_in_class: List[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        """Проверка наличия импорта allure."""
        for name in node.names:
            if name.name == "allure":
                self.has_allure_import = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Проверка наличия импорта из allure."""
        modules = ("allure", "allure_commons", "vedro_allure_reporter")
        if node.module in modules:
            self.has_allure_import = True
        self.generic_visit(node)

    def _is_scenario_class(self, node: ast.ClassDef) -> bool:
        """Проверяет, является ли класс наследником Scenario."""
        for base in node.bases:
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name):
                if base.value.id == "vedro" and base.attr == "Scenario":
                    return True
            elif isinstance(base, ast.Name) and base.id == "Scenario":
                return True
        return False

    def _check_decorators(self, node: ast.ClassDef) -> bool:
        """Проверяет наличие декоратора @allure.id() и собирает информацию о всех декораторах.

        Возвращает True, если декоратор @allure.id() найден.
        """
        has_allure_id = False
        self.decorators_in_class = []

        for decorator in node.decorator_list:
            if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
                continue

            if self._is_allure_id_decorator(decorator):
                has_allure_id = True

            # Собираем названия всех декораторов для информационных сообщений
            if isinstance(decorator.func.value, ast.Name):
                self.decorators_in_class.append(f"{decorator.func.value.id}.{decorator.func.attr}")

        return has_allure_id

    def _is_allure_id_decorator(self, decorator: ast.Call) -> bool:
        """Проверяет, является ли декоратор декоратором @allure.id()."""
        return (
            decorator.func.attr == "id"
            and isinstance(decorator.func.value, ast.Name)
            and decorator.func.value.id == "allure"
        )

    def _add_error_for_missing_decorator(self, node: ast.ClassDef) -> None:
        """Добавляет ошибку, если декоратор @allure.id() отсутствует."""
        if self.has_allure_import:
            # Импорт allure есть, но декоратора @allure.id() нет
            decorators_str = (
                ", ".join(self.decorators_in_class) if self.decorators_in_class else "нет"
            )
            self.errors.append(
                (
                    node.lineno,
                    node.col_offset,
                    f"UGC100 класс Scenario должен иметь декоратор @allure.id(). "
                    f"Найдены декораторы: {decorators_str}",
                    type(self),
                )
            )
        else:
            # Нет ни импорта allure, ни декоратора
            msg = (
                "UGC101 импортируйте allure и добавьте декоратор "
                "@allure.id() для класса Scenario"
            )
            self.errors.append(
                (
                    node.lineno,
                    node.col_offset,
                    msg,
                    type(self),
                )
            )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Посещение определения класса - основная логика проверки."""
        if self._is_scenario_class(node):
            has_allure_id = self._check_decorators(node)

            if not has_allure_id:
                self._add_error_for_missing_decorator(node)

        self.generic_visit(node)


class AllureIdPlugin:
    """Flake8 плагин для проверки наличия декоратора @allure.id() для классов Scenario."""

    name = "flake8-vedro-allure-id"
    version = "0.1.0"

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """Запуск проверки кода."""
        visitor = AllureIdVisitor()
        visitor.visit(self._tree)

        for line, col, msg, class_type in visitor.errors:
            yield line, col, msg, class_type
