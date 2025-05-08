import ast
import pytest
from flake8_vedro_allure_id_plugin.plugin import AllureIdPlugin, AllureIdVisitor


def _results(code_snippet):
    """Helper to run plugin on code snippet and return results."""
    tree = ast.parse(code_snippet)
    plugin = AllureIdPlugin(tree)
    return list(plugin.run())


def test_plugin_version():
    """Check that plugin version is defined."""
    assert AllureIdPlugin.version


def test_plugin_name():
    """Check plugin name."""
    assert AllureIdPlugin.name == "flake8-vedro-allure-id"


def test_error_when_missing_allure_import():
    """Check that error is reported when allure import is missing."""
    code = """
class Scenario:
    pass

class TestScenario(Scenario):
    pass
"""
    errors = _results(code)
    assert len(errors) == 1
    assert errors[0][2] == "UGC101 импортируйте allure и добавьте декоратор @allure.id() для класса Scenario"


def test_error_when_decorator_missing_with_import():
    """Check that error is reported when decorator is missing but allure is imported."""
    code = """
import allure

class Scenario:
    pass

class TestScenario(Scenario):
    pass
"""
    errors = _results(code)
    assert len(errors) == 1
    assert errors[0][2] == "UGC100 класс Scenario должен иметь декоратор @allure.id(). Найдены декораторы: нет"


def test_no_error_when_has_decorator():
    """Check that no error is reported when allure.id() decorator exists."""
    code = """
import allure

class Scenario:
    pass

@allure.id(123)
class TestScenario(Scenario):
    pass
"""
    errors = _results(code)
    assert len(errors) == 0


def test_no_error_for_non_scenario_class():
    """Check that no error is reported for classes not inheriting from Scenario."""
    code = """
import allure

class NotScenario:
    pass
"""
    errors = _results(code)
    assert len(errors) == 0


def test_error_lists_other_decorators():
    """Check that error message lists other decorators found on the class."""
    code = """
import allure

class Scenario:
    pass

@allure.feature("Test")
@allure.description("Description")
class TestScenario(Scenario):
    pass
"""
    errors = _results(code)
    assert len(errors) == 1
    assert "allure.feature, allure.description" in errors[0][2]


def test_imported_scenario():
    """Check that error is reported for an imported Scenario class."""
    code = """
import allure
import vedro

class TestScenario(vedro.Scenario):
    pass
"""
    errors = _results(code)
    assert len(errors) == 1
    assert "UGC100" in errors[0][2]


def test_visitor_gets_allure_import_from_import_from():
    """Check that AllureIdVisitor correctly detects allure imports from from-imports."""
    code = """
from allure import feature

class Scenario:
    pass

@feature("Test")
class TestScenario(Scenario):
    pass
"""
    tree = ast.parse(code)
    visitor = AllureIdVisitor()
    visitor.visit(tree)
    assert visitor.has_allure_import is True
    assert len(visitor.errors) == 1
    assert "UGC100" in visitor.errors[0][2]


def test_allure_commons_import():
    """Check that import from allure_commons is detected."""
    code = """
from allure_commons import feature

class Scenario:
    pass

@feature("Test")
class TestScenario(Scenario):
    pass
"""
    tree = ast.parse(code)
    visitor = AllureIdVisitor()
    visitor.visit(tree)
    assert visitor.has_allure_import is True


def test_vedro_allure_reporter_import():
    """Check that import from vedro_allure_reporter is detected."""
    code = """
from vedro_allure_reporter import feature

class Scenario:
    pass

@feature("Test")
class TestScenario(Scenario):
    pass
"""
    tree = ast.parse(code)
    visitor = AllureIdVisitor()
    visitor.visit(tree)
    assert visitor.has_allure_import is True 